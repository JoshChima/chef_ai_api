"""This module provides example tools for web scraping and search functionality.

It includes a basic Tavily search function (as an example)

These tools are intended as free examples to get started. For production use,
consider implementing more robust and specialized tools tailored to your needs.
"""

from typing import Any, Callable, List, Optional, cast

# from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnableConfig
from langsmith import traceable
from typing_extensions import Annotated

from chef_agent.state import ChefState
from chef_agent.utils import load_chat_model, format_docs
from chef_agent.configuration import Configuration
from chef_agent.prompts import SOURCE_EXPLAINATION_PROMPT

from langchain_openai import OpenAIEmbeddings
from langchain_chroma.vectorstores import Chroma
from langchain_graph_retriever.transformers import ShreddingTransformer
from langchain_graph_retriever.adapters.chroma import ChromaAdapter
from graph_retriever.strategies import Eager
from langchain_graph_retriever import GraphRetriever

from langchain_core.language_models import BaseChatModel
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
    RunnableParallel,
)

from langchain_core.tools import InjectedToolArg, tool
from langchain_core.tools.base import InjectedToolCallId
from langchain_core.messages import ToolMessage
from langgraph.types import Command, interrupt
from langgraph.prebuilt import InjectedState


################ Search Using Graph Retriever ################
def load_retriver():
    print("Loading Graph Retriever...")
    # print current working directory
    import os

    print(os.getcwd())
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    shredder = ShreddingTransformer()
    vector_store = ChromaAdapter(
        Chroma(
            embedding_function=embeddings,
            collection_name="recipe_qa_combined",
            persist_directory="./src/chef_agent/data/recipe_qa_combined_chroma_db",
        ),
        shredder,
        {"keywords"},
    )

    traversal_retriever = GraphRetriever(
        store=vector_store,
        edges=[("keywords", "keywords"), ("source_id", "source_id")],
        strategy=Eager(k=5, start_k=5, max_depth=3),
    )
    return traversal_retriever


@traceable(run_type="llm")
def source_explaination(question, docs: list[Document], config: RunnableConfig = None):
    configuration = Configuration.from_runnable_config(config)
    llm = load_chat_model(configuration.model)

    se_prompt = ChatPromptTemplate.from_template(SOURCE_EXPLAINATION_PROMPT)
    explaination_chain = se_prompt | llm | StrOutputParser()

    se_chain = RunnableParallel(
        question=RunnableLambda(lambda x: x["question"]),
        docs=RunnableLambda(lambda x: x["source"]),
        explaination=explaination_chain,
    )

    formatted_docs = [
        {"question": question, "source": doc, **format_docs(doc)} for doc in docs
    ]
    se_response = se_chain.batch(formatted_docs)
    return se_response


ss_seperator = f"\n{'#'*20}\n"


@tool
async def search(
    query: str,
    *,
    tool_call_id: Annotated[str, InjectedToolCallId],
    config: Annotated[RunnableConfig, InjectedToolArg],
):
    """Search for general web results.

    This function performs a search for relevent sources such as recipes and cooking related topics.
    """
    traversal_retriever = load_retriver()
    search_chain = (
        RunnableParallel(sources=traversal_retriever, question=RunnablePassthrough())
        | RunnablePassthrough.assign(
            explainations=RunnableLambda(
                lambda x: source_explaination(x["question"], x["sources"])
            )
        )
        | RunnablePassthrough.assign(
            search_summary=RunnableLambda(
                lambda x: f"{ss_seperator}Search Results:\n"
                + "\n".join([f"> {e['explaination']}" for e in x["explainations"]])
                + ss_seperator
            )
        )
    )
    response = await search_chain.ainvoke(query, config=config)
    return Command(
        update={
            "messages": [
                ToolMessage(
                    content=response["search_summary"],
                    tool_call_id=tool_call_id,
                )
            ],
            "documents": response["sources"],
            "is_post_search_step": True,
        }
    )

@tool
async def request_recipe_choice_from_sources( inferred_recipe_id: str, *, tool_call_id: Annotated[str, InjectedToolCallId], state: Annotated[ChefState, InjectedState],
    config: Annotated[RunnableConfig, InjectedToolArg]):
    """Request user select a recipe from search results

    This function requests the user to select a recipe from the search results, when required for the conversation.

    If a recipe is already inferred, request the user to confirm the recipe.
    """
    # Get all recipe documents from the state
    recipe_docs = [doc for doc in state.documents if doc.metadata.get("type") == "recipe"]

    # Check if there are any recipe documents in the state
    if len(recipe_docs) < 1:
        return {
            "messages": [
                ToolMessage(
                    content="There are no recipes to chooose from in the search results.",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    
    # If a recipe is already inferred, request the user to confirm the recipe
    if inferred_recipe_id:
        inferred_recipe = next((doc for doc in recipe_docs if doc.id == inferred_recipe_id), None)

        # Request user to confirm the inferred recipe
        inferred_recipe_message = f"""Are you looking to use the following recipe? Type ['yes', 'y'] to confirm or ['no', 'n'] to select a different recipe:
        {inferred_recipe.metadata['title']}
        """
        inferred_feedback = interrupt(inferred_recipe_message)
        if inferred_feedback.lower() in ['yes', 'y']:
            return {
                "messages": [
                    ToolMessage(
                        content=f"Great! You have selected recipe {inferred_recipe.metadata['title']}.",
                        tool_call_id=tool_call_id,
                    )
                ],
                "selected_recipe": inferred_recipe
            }
        elif inferred_feedback.lower() in ['no', 'n']:
            pass
        else:
            pass

    recipe_tag = []
    recipe_format = []
    for i, recipe in enumerate(recipe_docs):
        rf_tag = f"{i+1}. {recipe.metadata['title']}"
        rf = f"{rf_tag}\n{recipe.page_content}"
        recipe_tag.append(rf_tag)
        recipe_format.append(rf)
    
    recipe_contents = "\n".join(recipe_format)
    feedback_message = f"""Please select a recipe you would like to use from the search results:
    {recipe_contents}
    [{", ".join(recipe_tag)}]
    """
    feedback = interrupt(feedback_message)
    # attempt to cast feedback as int
    try:
        feedback = int(feedback)
        # check if feedback is within the range of recipes
        if feedback in range(1, len(recipe_docs)+1):
            return {
                "messages": [
                    ToolMessage(
                        content=f"Great! You have selected recipe {feedback}.",
                        tool_call_id=tool_call_id,
                    )
                ],
                "selected_recipe": recipe_docs[feedback-1]
            }
        else:
            return {
                "messages": [
                    ToolMessage(
                        content="Please enter the number corresponding to the recipe you would like to use.",
                        tool_call_id=tool_call_id,
                    )
                ]
            }
    except ValueError:
        return {
            "messages": [
                ToolMessage(
                    content="Please enter the number corresponding to the recipe you would like to use.",
                    tool_call_id=tool_call_id,
                )
            ]
        }
    



TOOLS: List[Callable[..., Any]] = [search, request_recipe_choice_from_sources]
