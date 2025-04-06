from typing import Optional
from datetime import datetime

from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from bcrypt import hashpw, checkpw, gensalt

from .role import Role

from libs import db

class User:
    def __init__(self,):
        self._id: ObjectId
        self.password: bytes
        self.email: str 
        self.role: Role 
        self.created_at: datetime 
        self.updated_at: datetime 

    @staticmethod
    def hash_password(password: str) -> bytes:
        return hashpw(password.encode("utf-8"), gensalt())

        
    @classmethod
    def new(cls, email: str, password: str, role: Role):
        user = cls()
        user.password = cls.hash_password(password)
        user.email = email
        user.role = role
        user.created_at = user.updated_at = datetime.now()

        res = db['users'].insert_one({
            "password": user.password,
            "email": user.email,
            "role_id": role._id,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        })

        user._id = res.inserted_id

        return user

    
    @classmethod
    def get(cls, id: Optional[ObjectId] = None, email: Optional[str] = None) -> "User":
        if __debug__:
            assert id is not None or email is not None, "Either 'id' or 'name' must be provided"
            if id is not None:
                assert isinstance(id, ObjectId), "'id' must be an ObjectId"
            if email is not None:
                assert isinstance(email, str), "'email' must be a string"
        
        query = {}

        if id:
            query["_id"] = id
        elif email:
            query["email"] = email

        data = db["users"].find_one(query)
        if data:
            user = cls()
            user._id = data["_id"]
            user.email = data["email"]
            user.role = Role.get(id=data["role_id"])
            user.password = data["password"]
            user.created_at = data["created_at"]
            user.updated_at = data["updated_at"]
            return user

        raise ValueError("User not found")

    def is_admin(self) -> "User":
        admin = Role.get(name="admin")
        print(self.role, admin)
        if self.role._id == admin._id:
            return self
        raise ValueError(f"User {self.email} is not an admin")

    def is_editor(self) -> "User":
        editor = Role.get(name="editor")
        if self.role._id == editor._id:
            return self 
        raise ValueError(f"User {self.email} is not an editor")


    def check_password(self, password: str) -> "User":
        if __debug__:
            assert isinstance(password, str), "'password' must be a string"
        if checkpw(password.encode("utf-8"), self.password):
            return self
        raise ValueError("Invalid password")

    def to_dict(self):
        return {
            "_id": self._id,
            "password": self.password,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
    
    def __repr__(self):
        return f"<User id={self._id} email={self.email}>"