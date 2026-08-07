from beanie import Document, PydanticObjectId
from pydantic import BaseModel


# class Category(BaseModel):
#     name: int
#     description: str

# class User(Document):
#     id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
#
#     class Settings:
#         name = "User"
#
#         -> Se quisermos associar a uma collection eexistente, fazemos dessa forma
#         criando um schema com os dados que queremos acessar ou associar daquela collection.
#         e usamos o tipo Link do beani para fazer a relação


# ================================================
# SCHEMA MONGODB WITH DOCUMENT OF BEANI
# ================================================
class Transaction(Document):
    user_id: PydanticObjectId
    amount: float
    type: str
    category: str
    description: str
    date: str

    class Settings:
        name = "transactions"


# ================================================
# SCHEMA REQ/RES WITH BASEMODEL OF PYDANTIC
# ================================================
class AntilisoPost(BaseModel):
    user_id: PydanticObjectId
    conversation_id: PydanticObjectId
    text: str

class AntilisoResponse(BaseModel):
    text: str