import click
from models import Role, User
from libs import db, setup_indexes, drop_collections


def register_commands(app):
    @app.cli.command("setup")
    def setup():
        """
        Setup the database.
        """
        print("Setting up database...")
        setup_indexes(db)

        admin_role = Role.new("admin")
        _ = Role.new("editor")

        print("Creating admin")
        email = click.prompt("Enter email")
        password = click.prompt("Enter password", hide_input=True)
        User.new(email=email, password=password, role=admin_role)
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
        drop_collections(db)
        print("All collections dropped.")