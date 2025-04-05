
from pymongo.errors import DuplicateKeyError
from models import Role
import pytest

def test_role_new(app):
    role: Role = Role.new("admin")
    assert role.name == "admin"
    assert role._id is not None


def test_duplicate_role(app):
    with pytest.raises(DuplicateKeyError):
        Role.new("admin")