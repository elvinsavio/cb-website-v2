import pytest

from pymongo.errors import DuplicateKeyError

from models import User


def test_user_new_admin(app, admin_role):
    password = "admin@123"
    user = User.new(email="admin@test.com", password=password, role=admin_role)
    assert isinstance(user, User)
    assert user.email == "admin@test.com"
    assert user.password != password
    assert user.role == admin_role
    assert user._id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.is_admin() == user

def test_user_new_editor(app, editor_role):
    password = "editor@123"
    user = User.new(email="editor@test.com", password=password, role=editor_role)
    assert isinstance(user, User)
    assert user.email == "editor@test.com"
    assert user.password != password
    assert user.role == editor_role
    assert user._id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert user.is_editor() == user
    
def test_user_check_password(app, admin_role):
    password = "admin@123"
    user = User.new(email="admin@test.com", password=password, role=admin_role)
    assert user.check_password(password) == user
    
def test_user_check_password_fail(app, admin_role):
    password = "admin@123"
    user = User.new(email="admin@test.com", password=password, role=admin_role)
    with pytest.raises(ValueError):
        user.check_password("wrong_password")

    
def test_duplicate_user(app, user, admin_role):
    with pytest.raises(DuplicateKeyError):
        User.new(email="admin@test.com", password="wrong_password", role=admin_role)
    