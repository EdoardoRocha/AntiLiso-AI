from pymongo import AsyncMongoClient
from beanie import init_beanie
from models.transactions_model import Transaction
import os

MONGO_URL = os.getenv("MONGO_URL")

async def init():

    try:
        client = AsyncMongoClient(MONGO_URL)
        await init_beanie(database=client.antiliso, document_models=[Transaction])
    except Exception as e:
        print(f'Failed to connect to MongoDB: {e}')