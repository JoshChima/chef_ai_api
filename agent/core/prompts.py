from langsmith import Client
from agent.utils import routes

"""Default prompts."""

client = Client()

ROUTER_SYSTEM_PROMPT = """Classify the best action route for answering the provided query.


<instructions>
    <instruction> Pick the best route from the provided options. Only pick routes from the list and return their `route_name`. </instruction>
    <instruction> If the best route is to prepare a search query, pick the best search scope from the provided options. Only pick search scopes from the list and return their `search_scope_type_name`. </instruction>
</instructions>

Routes:
<routes>
    <route>
        <name>search</name>
        <description>Prepare to search for more information that helps answer the query if needed.</description>
    </route>
    <route>
        <name>ingredient_check</name>
        <description> Identify that from the provided ingredients in the query, if there are enough ingredients to prepare the provided recipe. </description>
    </route>
    <route>
        <name>ask_user_info</name>
        <description> Ask the user for more information to help answer the query. </description>
    </route>
    <route>
        <name>review_and_reflect</name>
        <description> Review the information and reflect on the query. </description>
    </route>
</routes>
Search Scope Types:
<search_scope_types>
    <search_scope_type>
        <name> recipe </name>
        <description> The search is about a specific recipe and should only be limited to that recipe or other sources relevant to it. </description>
    </search_scope_type>
    <search_scope_type>
        <name> all </name>
        <description>Search for information that helps answer the query through all available recipes.</description>
    </search_scope_type>
</search_scope_types>
"""
