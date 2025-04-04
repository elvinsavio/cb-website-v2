from datetime import datetime

from libs import db

from pymongo import ObjectId

class Role:
    def __init__(self,):
        self._id: ObjectId | None = None
        self.name: str | None = None
        self.created_at: datetime | None = None
        self.updated_at: datetime | None = None

    @classmethod
    def new(cls, name: str):
        if __debug__:
            assert name is not None, "name is required"
            assert isinstance(name, str), "name must be a string"
            assert len(name) > 0, "name must be a non-empty string"
            assert len(name) < 255, "name must be less than 255 characters"
        role = cls()
        role.name = name
        role.created_at = role.updated_at = datetime.now()
        return role
    
    @classmethod
    def get(cls, id: ObjectId):
        if __debug__:
            assert id is not None, "id is required"
            assert isinstance(id, ObjectId), "id must be an ObjectId"
        
        data = db.roles.find_one({"_id": id})
        if data:
            role = cls()
            role._id = data["_id"]
            role.name = data["name"]
            role.created_at = data["created_at"]
            role.updated_at = data["updated_at"]
            return role
        return None