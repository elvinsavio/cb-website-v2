import click
from models import Role
from libs import db
from models.user import User

def register_commands(app):
    @app.cli.command("setup")
    def setup(test: bool = False):
        """
        Setup the database.
        """
        print("Setting up database...")
        db.roles.create_index("name", unique=True)
        db.users.create_index("username", unique=True)
        db.users.create_index("email", unique=True)
        db.users.create_index("role_id")

        admin_role = Role.new("admin")
        _ = Role.new("editor")

        print("Creating admin")
        email = click.prompt("Enter email")
        password = click.prompt("Enter password", hide_input=True)
        User.new("admin", password, email, admin_role)
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