from typing import Optional

from datetime import datetime


from libs import db

from bson import ObjectId
from pymongo.errors import DuplicateKeyError


class Role:
    def __init__(
        self,
    ):
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

        res = db["roles"].insert_one(
            {
                "name": name,
                "created_at": now,
                "updated_at": now,
            }
        )

        role = cls()
        role._id = res.inserted_id
        role.name = name
        role.created_at = now
        role.updated_at = now

        return role

    @classmethod
    def get(cls, id: Optional[ObjectId] = None, name: Optional[str] = None):
        if __debug__:
            assert id is not None or name is not None, "Either 'id' or 'name' must be provided"
            if id is not None:
                assert isinstance(id, ObjectId), "'id' must be an ObjectId"
            if name is not None:
                assert isinstance(name, str), "'name' must be a string"
        
        query = {}
        if id:
            query["_id"] = id
        elif name:
            query["name"] = name

        data = db.roles.find_one(query)
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
