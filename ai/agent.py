from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from ai.prompt import system_prompt
from ai.memory.memory import checkpointer
from langchain.agents.middleware import SummarizationMiddleware
from dotenv import load_dotenv

load_dotenv()

from ai.tools.transactions_tools import inserir_transacao, buscar_transacoes, executar_agregacao_mongo

llm = init_chat_model("openai:gpt-4o-mini")
antiliso_agent = create_agent(
    model=llm,
    system_prompt=system_prompt,
    tools=[inserir_transacao, buscar_transacoes, executar_agregacao_mongo],
    checkpointer=checkpointer,
    middleware=[SummarizationMiddleware(
        model=llm,
        trigger=("tokens", 5000),
        keep=("messages", 6)
    )],
)
