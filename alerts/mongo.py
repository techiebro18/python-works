import pymongo
from pymongo import MongoClient
from decouple import config

def get_database(**kwargs):
    connection_string = config('CONNECTION_STRING')
    client = MongoClient(connection_string)
    dbname = kwargs.get('dbname', 'demo')
    return client[dbname]


        
