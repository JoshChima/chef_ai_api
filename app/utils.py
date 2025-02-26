"""Shared utility functions used in the project.

Functions:
    format_docs: Convert documents to an xml-formatted string.
"""

import uuid
from typing import Any, Literal, Optional, Union

from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel

search_scope_type = {
                "search_scope_type": [
                    {"recipe": "Only search for information regarding a single recipe"},
                    {"all": "Search through all available recipes"},
                ]
            }

routes = {
    "prepare_search_query": {
        "router_description": "Search for information regarding recipes",
        "params": [
            search_scope_type
        ],
    },
    "ingredient_check": {"search_scope_type": None},
}
