
from pymongo.errors import DuplicateKeyError
from models import Role
import pytest

def test_role_new_admin(app):
    role: Role = Role.new("admin")
    assert isinstance(role, Role)
    assert role.name == "admin"
    assert role._id is not None

def test_role_new_editor(app):
    role: Role = Role.new("editor")
    assert isinstance(role, Role)
    assert role.name == "editor"
    assert role._id is not None

def test_duplicate_role(app, admin_role, editor_role):
    with pytest.raises(DuplicateKeyError):
        Role.new("admin")
    with pytest.raises(DuplicateKeyError):
        Role.new("editor")