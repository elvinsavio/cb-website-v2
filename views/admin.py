from flask import flash, request, redirect, Blueprint, url_for, render_template

from libs import FormBuilder

from models import User

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.get("/")
def admin_lage():
    header = request.headers.get("Authorization")
    if header is None:
        return redirect(url_for("admin.login_page"))
    return "Admin page"

@admin_blueprint.get("/login")
def login_page():

    form = FormBuilder()

    form.add_field("email", "text", "Email", required=True)
    form.add_field("password", "password", "Password", required=True)
    form.add_button("login", "submit", "Login")

    return render_template("admin/login.html", form=form.render())


@admin_blueprint.post("/api/login")
def login():
    
    email, password = request.form.get("email"), request.form.get("password")

    if email is None or password is None:
        flash("Please fill in all fields", "warning")
        return redirect(url_for("admin.login_page")) 

    try:
        user = User.get(email=email).check_password(password)
    except Exception as e:
        flash(e.args[0], "error")
        return redirect(url_for("admin.login_page"))
    
    
    print(user)

    
    return redirect(url_for("admin.login_page"))