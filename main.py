from libs import config

from flask import Flask

from cli import register_commands

app = Flask(__name__)
register_commands(app)

if __name__ == "__main__":
    app.run(debug=config.debug)