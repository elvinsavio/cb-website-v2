import pytest

from main import create_app

from libs import setup_indexes, drop_collections, db


@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    print("setting")
    with app.app_context():
        drop_collections(db)
        setup_indexes(db)
        yield app
        
        