from flask import request, redirect, Blueprint, url_for, render_template

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.get("/")
def admin():
    header = request.headers.get("Authorization")
    if header is None:
        return redirect(url_for("admin.login"))
    return "Admin page"

@admin_blueprint.get("/login")
def login():
    return render_template("admin/login.html")