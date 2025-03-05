"""
Main graph module that containes the conversational agent graph.
"""

from typing import Any, Literal, TypedDict, cast

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph

from agent.core.state import QueryRouter, ChefState
from agent.core.prompts import ROUTER_SYSTEM_PROMPT
from langchain.chat_models import init_chat_model

# async def analyze_and_delegate(state: ChefState, config: RunnableConfig) -> dict[str, QueryRouter]:
#     """Analyze the user query and delegate to the appropriate node.

#     Args:
#         state: The current state of the agent.
#         config: The configuration for the agent.
    
#     Returns:
#         dict[str, QueryRouter]: A dictionary containing the router key with the classification results.
#     """

#     # TODO: Router Override Logic

#     # load chat model
#     model = init_chat_model("gpt-4o-mini", model_provider="openai")

#     messages = [
#         {"role": "system", "content": ROUTER_SYSTEM_PROMPT}
#     ] + state.messages
#     response = cast(
#         QueryRouter, await model.with_structured_output(QueryRouter).ainvoke(messages)
#     )
#     return {"router": response}

async def search(state: ChefState, config: RunnableConfig) -> str:
    """Search for information regarding recipes.

    Args:
        state: The current state of the agent.
        config: The configuration for the agent.
    
    Returns:
        str: The search results.
    """
    return "search"
