"""State management.

This module defines the state structures used by the conversational agent.

sources: https://github.com/langchain-ai/chat-langchain/blob/master/backend/retrieval_graph/state.py
"""

from dataclasses import dataclass, field
from typing import Annotated, Literal, Optional

from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from typing_extensions import TypedDict

@dataclass(kw_only=True)
class InputState:
    """Represent the structure of the input state.

    This class defines the structure of accepted inputs that can be passed in externally from the user or upstream services.

    messages: A list of messages from current conversation.
    ingredients (optional): A list of ingredients tags to query on.
    recipe (optional): A recipe to be used in scope of the query.
    """

    messages: Annotated[list[AnyMessage], add_messages]
    ingredients: list[str] = field(default_factory=list)
    recipe: Optional[Document] = None

@dataclass(kw_only=True)
class OutputResponse(TypedDict):
    answer: str    
    sources: list[Document]

class QueryRouter(TypedDict):
    """Classify user query"""

    type: Literal["search", "ingredient_check", "ask_user_info", "review_and_reflect"]
    search_scope_type: Optional[Literal["recipe", "all"]]

class QueryRouterOverride(QueryRouter):
    """Additional Route Parameters"""

    # Optional, for nodes that call 
    route_override: str

class ChefState(InputState):
    """State of the chef agent."""
    
    query_router: QueryRouter = field(default_factory=lambda: QueryRouter(type="prepare_search_query", search_scope_type="all"))
    """The router's classification for the query."""

    documents: list[Document] = field(default_factory=list)
    """Populated documents from retrieval nodes."""

    answer: Optional[OutputResponse] = None


