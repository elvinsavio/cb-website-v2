from libs import config

from flask import Flask

from cli import register_commands

from views import admin_blueprint

def create_app():
    app = Flask(__name__)
    register_commands(app)
    app.register_blueprint(admin_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=config.debug)