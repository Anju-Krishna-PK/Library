# Establish database connection

from pymongo import MongoClient

conn = MongoClient("mongodb://localhost:27017/")
db = conn["library"]
books_collection = db["Book"]
customers_collection = db["User"]