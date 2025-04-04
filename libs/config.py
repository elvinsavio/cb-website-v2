import os
import dotenv
from flask import g
from werkzeug.local import LocalProxy


class Config:
    def __init__(self):
        dotenv.load_dotenv()

        self.name = os.getenv("APP_NAME")
        self.env = os.getenv("FLASK_ENV", "development")
        self.debug = self.env == "development"
        self.secret_key = os.getenv("SECRET_KEY")
        self.mongo_uri = os.getenv("MONGO_URI")
        self.mongo_db = os.getenv("MONGO_DB")
        self.mongo_user = os.getenv("MONGO_USER")
        self.mongo_password = os.getenv("MONGO_PASSWORD")
        

        if __debug__:
            assert self.name is not None, "APP_NAME is not set"
            assert self.env in ["development", "production"], "Invalid environment"
            assert self.secret_key is not None, "SECRET_KEY is not set"
            assert self.mongo_uri is not None, "MONGO_URI is not set"
            assert self.mongo_db is not None, "MONGO_DB is not set"
            assert self.mongo_user is not None, "MONGO_USER is not set"
            assert self.mongo_password is not None, "MONGO_PASSWORD is not set"



config = Config()