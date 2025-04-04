from flask import g
from werkzeug.local import LocalProxy
import pymongo
from libs import config

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        mongo_uri = f"mongodb+srv://{config.mongo_user}:{config.mongo_password}@{config.mongo_uri}/?retryWrites=true&w=majority&appName=cluster"    
        client = pymongo.MongoClient(mongo_uri)

        db = client[config.mongo_db]

        g._database = db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)