from libs import config
from cmd import register_commands

from flask import Flask


app = Flask(config.name)
register_commands(app)

if __name__ == "__main__":
    app.run(debug=config.debug)