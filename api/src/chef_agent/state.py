"""State management.

This module defines the state structures used by the conversational agent.

sources: https://github.com/langchain-ai/chat-langchain/blob/master/backend/retrieval_graph/state.py
"""

from dataclasses import dataclass, field
from typing import Annotated, Literal, Optional, Sequence

from langchain_core.documents import Document
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep
from typing_extensions import TypedDict

@dataclass
class InputState:
    """Represent the structure of the input state.

    This class defines the structure of accepted inputs that can be passed in externally from the user or upstream services.

    messages: A list of messages from current conversation.
    ingredients (optional): A list of ingredients tags to query on.
    recipe (optional): A recipe to be used in scope of the query.
    """

    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    selected_ingredients: Optional[list[str]] = field(default_factory=list)
    selected_recipe: Optional[Document] = None

@dataclass(kw_only=True)
class OutputResponse(TypedDict):
    answer: str    
    sources: list[Document]

# class QueryRouter(TypedDict):
#     """Classify user query"""

#     type: Literal["search", "ingredient_check", "ask_user_info", "review_and_reflect"]
#     search_scope_type: Optional[Literal["recipe", "all"]]

# class QueryRouterOverride(QueryRouter):
#     """Additional Route Parameters"""

#     # Optional, for nodes that call 
#     route_override: str

@dataclass
class ChefState(InputState):
    """State of the chef agent."""
    
    # query_router: QueryRouter = field(default_factory=lambda: QueryRouter(type="prepare_search_query", search_scope_type="all"))
    # """The router's classification for the query."""

    documents: list[Document] = field(default_factory=list)
    """Populated documents from retrieval nodes."""

    # answer: Optional[OutputResponse] = None

    is_post_search_step: bool = field(default=False)

    is_last_step: IsLastStep = field(default=False)
    """
    Indicates whether the current step is the last one before the graph raises an error.

    This is a 'managed' variable, controlled by the state machine rather than user code.
    It is set to 'True' when the step count reaches recursion_limit - 1.
    """


