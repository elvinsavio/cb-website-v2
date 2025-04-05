import pytest

from main import create_app

from libs import setup_indexes, drop_collections, db
from models.role import Role


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        drop_collections(db)
        setup_indexes(db)
        yield app
        

@pytest.fixture
def admin_role():
    return Role.new("admin")

@pytest.fixture
def editor_role():
    return Role.new("editor")