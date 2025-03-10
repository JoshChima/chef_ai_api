"""Utility & helper functions."""

from typing import Union
from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document
from langsmith import traceable


def get_message_text(msg: BaseMessage) -> str:
    """Get the text content of a message."""
    content = msg.content
    if isinstance(content, str):
        return content
    elif isinstance(content, dict):
        return content.get("text", "")
    else:
        txts = [c if isinstance(c, str) else (c.get("text") or "") for c in content]
        return "".join(txts).strip()


def load_chat_model(fully_specified_name: str) -> BaseChatModel:
    """Load a chat model from a fully specified name.

    Args:
        fully_specified_name (str): String in the format 'provider/model'.
    """
    provider, model = fully_specified_name.split("/", maxsplit=1)
    return init_chat_model(model, model_provider=provider)

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