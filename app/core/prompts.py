from langsmith import Client
from app.utils import routes
"""Default prompts."""

client = Client()

ROUTER_SYSTEM_PROMPT = """
Goal: Classify the best action route for answering the provided query.

<instructions>
- Pick the best route from the provided options. Only pick routes from the list and return their `route_name`.
- If the best route is to prepare a search query, pick the best search scope from the provided options. Only pick search scopes from the list and return their `search_scope_type`.
</instructions>

Search Scope Types Definitions:
1. `recipe`: Only search for information regarding a single recipe.
2. `all`: Search for information through all available recipes.
"""