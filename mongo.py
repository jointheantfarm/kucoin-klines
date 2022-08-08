from pymongo import MongoClient

from settings import MONGO_URL, MONGO_PORT

client = MongoClient(MONGO_URL, MONGO_PORT)