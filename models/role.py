from datetime import datetime

from libs import db

from bson import ObjectId
from pymongo.errors import DuplicateKeyError

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

        now = datetime.now()
        try:
            res = db.roles.insert_one({
                "name": name,
                "created_at": now,
                "updated_at": now,
            })
        except DuplicateKeyError:
            raise ValueError(f"Role with name '{name}' already exists")

        role = cls()
        role._id = res.inserted_id
        role.name = name
        role.created_at = now
        role.updated_at = now

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


    def to_dict(self):
        return {
            "_id": self._id,
            "name": self.name,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __repr__(self):
        return f"<Role id={self._id} name={self.name}>"