import click
from models import Role
from libs import db

def register_commands(app):
    @app.cli.command("setup")
    def setup(test: bool = False):
        """
        Setup the database.
        """
        print("Setting up database...")
        db.roles.create_index("name", unique=True)
        Role.new("admin")
        Role.new("editor")
        print("Database setup complete.")
        
    @app.cli.command("drop-all")
    def drop_all():
        """
        Drop all collections.
        """
        print("Are you sure you want to drop all collections?")
        if not click.confirm("Continue?"):
            print("Aborting.")
            return

        print("Dropping all collections...")
        db.roles.drop()
        print("All collections dropped.")