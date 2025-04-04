from datetime import datetime
from pymongo import ObjectId


class User:
    def __init__(self,):
        self._id: ObjectId | None = None
        self.username: str | None = None
        self.password: str | None = None
        self.email: str | None = None
        self.role: str | None = None
        self.created_at: str | None = None
        self.updated_at: str | None = None

        
    @classmethod
    def new(cls, username: str, password: str, email: str, role: str):
        user = cls()
        user.username = username
        user.password = password
        user.email = email
        user.role = role
        user.created_at = user.updated_at = datetime.now()
        return user