from datetime import datetime

from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from bcrypt import hashpw, checkpw, gensalt

from .role import Role

from libs import db

class User:
    def __init__(self,):
        self._id: ObjectId | None = None
        self.username: str | None = None
        self.password: bytes | None = None
        self.email: str | None = None
        self.role: ObjectId | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

    @staticmethod
    def hash_password(password: str) -> bytes:
        return hashpw(password.encode("utf-8"), gensalt())

        
    @classmethod
    def new(cls, username: str, password: str, email: str, role: Role):
        user = cls()
        user.username = username
        user.password = cls.hash_password(password)
        user.email = email
        user.role = role._id
        user.created_at = user.updated_at = datetime.now()

        try:
            res = db.users.insert_one({
                "username": user.username,
                "password": user.password,
                "email": user.email,
                "role_id": role._id,
                "created_at": user.created_at,
                "updated_at": user.updated_at
            })
        except DuplicateKeyError:
            raise ValueError(f"User with username '{username}' already exists")

        user._id = res.inserted_id

        return user

