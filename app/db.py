from gc import collect
import pymongo
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()

UTDBOT_DB = os.getenv('MONGODB_URI')
cluster = None
db = None
collection = None


def start_db():
    global cluster, db ,collection
    
    cluster = MongoClient(UTDBOT_DB)
    db = cluster["mikkoro"]
    collection = db["utdbot"]

def close_db():
    global cluster
    
    cluster.close()

def check_connection():
    start_db()
    global collection
    
    try:
        collection = db["utdbot"]
    except:
        start_db()

def update_data(type,data,date):
    check_connection()
    
    query = {
        "type":type
    }
    
    to_update = {
        "$set": {
            "data": data,
            "date": date
        }
    }
    
    collection.update_one(query,to_update)
    
def find_data(type,date):
    check_connection()
    
    to_find = {
        "type": type,
        "date": date
    }
    
    response = collection.find_one(to_find)
    
    return response