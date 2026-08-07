from beanie import PydanticObjectId
from langchain.tools import tool
from models.transactions_model import Transaction

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
    :return: Uma mensagem de sucesso ou de falha da persistência no banco de dados
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
        return f"A transação foi cadastrada com sucesso!"
    except Exception as error:
        return f"Não foi possível cadastrar a transação no banco: {repr(error)}"
