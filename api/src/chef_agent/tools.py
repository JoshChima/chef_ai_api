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
from langgraph.types import Command

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
        {"keywords"}
    )

    traversal_retriever = GraphRetriever(
        store = vector_store,
        edges = [("keywords", "keywords"), ("source_id", "source_id")],
        strategy = Eager(k=5, start_k=5, max_depth=3),
    )
    return traversal_retriever

@traceable(run_type="llm")
def source_explaination(question, docs: list[Document], config:RunnableConfig=None):
    configuration = Configuration.from_runnable_config(config)
    llm = load_chat_model(configuration.model)

    se_prompt = ChatPromptTemplate.from_template(SOURCE_EXPLAINATION_PROMPT)
    explaination_chain = se_prompt | llm | StrOutputParser()

    se_chain = RunnableParallel(
        question=RunnableLambda(lambda x: x["question"]),
        docs=RunnableLambda(lambda x: x["source"]),
        explaination=explaination_chain
    )

    formatted_docs = [{"question":question, "source": doc, **format_docs(doc)} for doc in docs]
    se_response = se_chain.batch(formatted_docs)
    return se_response

ss_seperator = f"\n{'#'*20}\n"

@tool
async def search(
    query:str, *, tool_call_id: Annotated[str, InjectedToolCallId], config: Annotated[RunnableConfig, InjectedToolArg]
):
    """Search for general web results.

    This function performs a search for relevent sources such as recipes and cooking related topics.
    """
    traversal_retriever = load_retriver()
    search_chain = (
        RunnableParallel(sources=traversal_retriever, question=RunnablePassthrough())
        | RunnablePassthrough.assign(explainations=RunnableLambda(lambda x: source_explaination(x["question"], x["sources"])))
        | RunnablePassthrough.assign(
            search_summary=RunnableLambda(
                lambda x: f"{ss_seperator}Search Results:\n" + "\n".join([f"> {e['explaination']}" for e in x['explainations']]) + ss_seperator))
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
            "is_post_search_step": True
        }
    )


TOOLS: List[Callable[..., Any]] = [search]
