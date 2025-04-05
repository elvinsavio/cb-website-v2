import pytest

from pymongo.errors import DuplicateKeyError

from models import User


def test_user_new_admin(app, admin_role):
    assert admin_role is not None, "Admin role not found"
    password = "admin@123"
    user = User.new("admin", password, "admin@test.com", admin_role) 
    assert isinstance(user, User)
    assert user.username == "admin"
    assert user.email == "admin@test.com"
    assert user.password != password
    assert user.role == admin_role._id
    assert user._id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.is_admin()

def test_user_new_editor(app, editor_role):
    assert editor_role is not None, "Editor role not found"
    password = "editor@123"
    user = User.new("editor", password, "editor@test.com", editor_role) 
    assert isinstance(user, User)
    assert user.username == "editor"
    assert user.email == "editor@test.com"
    assert user.password != password
    assert user.role == editor_role._id
    assert user._id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert not user.is_admin()

def test_duplicate_user(app, admin_role):
    assert admin_role is not None, "Admin role not found"
    password = "admin@123"
    _: User = User.new("admin", password, "admin@test.com", admin_role)
    with pytest.raises(DuplicateKeyError):
        User.new("admin", password, "admin@test.com", admin_role) 
    