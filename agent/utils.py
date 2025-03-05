"""Shared utility functions used in the project.

Functions:
    format_docs: Convert documents to an xml-formatted string.
"""

import uuid
from typing import Any, Literal, Optional, Union

from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langsmith import traceable

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

@traceable(run_type="chain")
def format_docs(docs: Union[list[Document], Document], config=None):
    if isinstance(docs, Document):
        docs = [docs]
    print(docs)
    # formatted_docs = []
    # for doc in docs:
    #     doc_type = doc.metadata.get("type")
    #     f_doc = f"text: {doc.page_content} metadata: {doc.metadata}"
    #     if doc_type == "recipe":
    return {
        "context": "\n\n".join(
            f"text: {doc.page_content} metadata: {doc.metadata}" for doc in docs
        )
    }

def load_chat_model(fully_specified_name: str=None) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    if fully_specified_name is None:
        provider = "openai"
        model = "gpt-4o-mini"
    elif "/" in fully_specified_name:
        provider, model = fully_specified_name.split("/", maxsplit=1)
    else:
        provider = ""
        model = fully_specified_name

    model_kwargs = {"temperature": 0}
    if provider == "google_genai":
        model_kwargs["convert_system_message_to_human"] = True
    return init_chat_model(model, model_provider=provider, **model_kwargs)