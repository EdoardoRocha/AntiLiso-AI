from beanie import PydanticObjectId
from langchain.tools import tool
from config.database import MONGO_URL
from models.transactions_model import Transaction
from bson import ObjectId
import json
from pymongo import AsyncMongoClient
import os


@tool
async def executar_agregacao_mongo(pipeline_json: str, user_id: str) -> str:
    """
    Executa um pipeline de agregação no MongoDB na coleção 'transactions'.
    :param pipeline_json: String no formato JSON representando uma lista de estágios do MongoDB pipeline.
                       Exemplo: '[{"$match": {"type": "expense"}}, {"$group": {"_id": "$category", "total": {"$sum": "$amount"}}}]'
           user_id: ID do usuário que está conversando.
    :return: String no formato JSON com os registros no MongoDB pipeline.
    """

    try:
        client = AsyncMongoClient(MONGO_URL)
        db = client["antiliso"]
        collection = db["transactions"]

        pipeline = json.loads(pipeline_json)

        user_object_id = ObjectId(user_id)

        pipeline.insert(0, {
            "$match": {"user_id": user_object_id}
        })

        cursor = await collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)

        for doc in results:
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            if "user_id" in doc:
                doc["user_id"] = str(doc["user_id"])
        await client.close()
        return json.dumps(results, ensure_ascii=False)

    except Exception as error:
        return f"Erro ao executar a agregação no banco de dados. {str(repr(error))}"


@tool
async def inserir_transacao(user_id: PydanticObjectId,
                            amount: float,
                            type: str,
                            category: str,
                            description: str,
                            date: str):
    """
    Função responsável por inserir uma transação no banco de dados.
    Use quando o usuário falar que fez alguma transação.
    :param user_id: ID do usuário que fez a transação
    :param amount: Valor total da transação
    :param type: Tipo da transação. Só pode ser: "SPENT or GAIN"
    :param category: Categorya da transaçõo: Salário, comida, conta de luz...
    :param description: Uma breve descrição daquela transação
    :param date: A data da transação
    :return: Uma mensagem avisando o sucesso ou a falha da persistência no banco de dados.
    """
    try:
        nova_transaction = Transaction(
            user_id=user_id,
            amount=amount,
            type=type,
            category=category,
            description=description,
            date=date
        )

        await nova_transaction.create()
        return "A transação foi cadastrada com sucesso"
    except Exception as error:
        print({"status": 500, "data": f"Não foi possível cadastrar a transação no banco: {repr(error)}"})
        return "Não foi possível cadastrar a transação no banco de dados."


@tool
async def buscar_transacoes(user_id: PydanticObjectId):
    """
    Função que busca todas as transações do usuário registradas no banco.
    Use para quando precisar checar as transações que foram feitas anteriormente e quando o usuário
    pedir para ver.
    :param user_id: ID para ver somente as transações do usuário atual.
    :return: Lista com as transações encontradas no banco de dados ou mensagem informando a ausência de transações.
    """
    try:
        if not (result := await Transaction.find(Transaction.user_id == user_id).to_list()):
            return f"Não existe nenhuma transação cadastrada associada ao usuário. Avise-o de forma amigável que ele não possui transações cadastradas."
        return result

    except Exception as error:
        print({"status": 500, "message": f"Erro interno no servidor. {repr(error)}"})
        return "Não foi possível buscar as transações no banco por um erro interno."
