from flask import g, current_app
from werkzeug.local import LocalProxy
import pymongo
from libs import config

def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        mongo_uri: str = f"mongodb+srv://{config.mongo_user}:{config.mongo_password}@{config.mongo_uri}/?retryWrites=true&w=majority&appName=cluster"    
        client = pymongo.MongoClient(mongo_uri)
        if not config.mongo_db:
            raise ValueError("Database name (config.mongo_db) must be a valid string.")

        db_name = config.mongo_db
        if current_app.config.get("TESTING", False):
            db_name =  db_name + "_test"
            
        db = client[db_name]

        g._database = db
       
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def setup_indexes(_db):
    _db.roles.create_index("name", unique=True)
    _db.users.create_index("username", unique=True)
    _db.users.create_index("email", unique=True)

def drop_collections(_db):
    _db.roles.drop()
    _db.users.drop()