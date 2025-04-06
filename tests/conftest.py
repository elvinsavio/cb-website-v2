import pytest

from main import create_app

from libs import setup_indexes, drop_collections, db
from models import Role, User

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        setup_indexes(db)
        yield app
        drop_collections(db)
        
@pytest.fixture
def admin_role():
    return Role.new("admin")

@pytest.fixture
def editor_role():
    return Role.new("editor")


@pytest.fixture
def user(app, admin_role):
    password = "admin@123"
    return User.new(email="admin@test.com", password=password, role=admin_role)