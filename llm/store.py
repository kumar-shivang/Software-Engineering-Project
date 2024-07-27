from typing import Any, Dict, List

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pymongo import MongoClient


# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_history_db"]
collection = db["session_histories"]


# Helper function to convert chat history to/from dictionary
def chat_history_to_dict(history: BaseChatMessageHistory) -> Dict[str, Any]:
    return {
        "messages": [
            {"type": msg.type, "data": msg.content} for msg in history.messages
        ]
    }


def dict_to_chat_history(data: Dict[str, Any]) -> BaseChatMessageHistory:
    history = InMemoryChatMessageHistory()
    for msg in data["messages"]:
        if msg["type"] == "human":
            history.add_user_message(msg["data"])
        elif msg["type"] == "ai":
            history.add_ai_message(msg["data"])
    return history


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    session = collection.find_one({"session_id": session_id})
    if session is None:
        history = InMemoryChatMessageHistory()
        collection.insert_one(
            {"session_id": session_id, "history": chat_history_to_dict(history)}
        )
    else:
        history = dict_to_chat_history(session["history"])
    return history


def save_session_history(session_id: str, history: BaseChatMessageHistory) -> None:
    collection.update_one(
        {"session_id": session_id}, {"$set": {"history": chat_history_to_dict(history)}}
    )

