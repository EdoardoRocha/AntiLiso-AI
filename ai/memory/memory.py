import os
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo import MongoClient

mongo_url = os.getenv("MONGO_URL")
cliente = MongoClient(mongo_url)

checkpointer = MongoDBSaver(
    cliente,
    db_name="antiliso",
    checkpoint_name="checkpoints",
)