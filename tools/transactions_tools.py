from pymongo import MongoClient
from langchain_core.tools import tool
from dotenv import load_dotenv
from bson.objectid import ObjectId
from models.transactions import TransacaoSchema
from datetime import datetime, timezone
from langchain_core.runnables import RunnableConfig
import os

load_dotenv()


@tool(args_schema=TransacaoSchema)
def inserir_transacao(
        amount: float,
        type: str,
        category: str,
        description: str,
        date: str,
        config: RunnableConfig):
    """
    Essa função será usada para inserir uma transação feita pela usuário
    use quando ele disser que gastou ou que recebeu dinheiro.
    :param amount: valor da transação
    :param type: tipo da transação (gasto ou ganho)
    :param category: category da transação (comida, salário...)
    :param description: uma breve descrição
    :param date: data da transação
    :return:  mensagem de sucesso ou falha na transação
    """

    configuracoes = config.get("configurable", {})
    user_id = configuracoes.get("user_id")

    if not user_id:
        return "Falha intera: user_id não foi recebido no bloco 'configurable' do JSON."

    MONGO_URL = os.getenv("MONGO_URL_TRANSACTIONS")
    if not MONGO_URL:
        return f"Não foi possível se conectar ao banco de dados, pois a variável de ambiente está ausente."

    try:
        client = MongoClient(MONGO_URL)

        db = client.antiliso
        transaction = db.transactions

        try:
            id_do_usuario = ObjectId(user_id)
        except Exception as e:
            return "Falha: O user_id não é um formato válido de ObjectID."

        agora = datetime.now(timezone.utc)

        nova_transacao = {
            "user_id": id_do_usuario,
            "amount": amount,
            "type": type,
            "category": category,
            "description": description,
            "date": date,
            "createdAt": agora,
            "updatedAt": agora
        }

        transaction.insert_one(nova_transacao)

        return f"Dados da transação inseridas com sucesso no banco de dados!"
    except Exception as e:
        return f"Não foi possível cadastrar informações no banco: {e}"
