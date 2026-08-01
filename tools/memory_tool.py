from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
import os

from agent import agent_executor

MONGO_URL = os.getenv("MONGO_URL")
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Sempre que o agente precisar do histórico de um session_id, ele vai buscar (ou criar) os
    documentos nesta coleção do MongoDB"""
    return MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string=MONGO_URL,
        database_name="antiliso-ai",
        collection_name="sessions",
    )

agent_with_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="output",
)