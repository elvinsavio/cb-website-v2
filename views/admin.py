import datetime

import jwt
from flask import flash, request, redirect, Blueprint, url_for, render_template, make_response

from libs import FormBuilder, config

from models import User

admin_blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@admin_blueprint.get("/")
def admin_page():
    token = request.cookies.get("access_token")
    if not token:
        return redirect(url_for("admin.login_page"))
    
    try:
        user_data = jwt.decode(token, config.jwt_secret, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        flash("Session expired. Please login again.", "warning")
        return redirect(url_for("admin.login_page"))
    except jwt.InvalidTokenError:
        flash("Invalid token. Please login again.", "error")
        return redirect(url_for("admin.login_page"))

    # Optionally fetch user with payload['user_id']
    return render_template("admin/dashboard.html", email=user_data["email"])

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
    
    payload = {
        "user_id": str(user._id),
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, config.jwt_secret, algorithm="HS256")

    # Create response with cookie
    resp = make_response(redirect(url_for("admin.admin_page")))  # or wherever you want to redirect
    resp.set_cookie("access_token", token, httponly=True, secure=True, samesite='Lax')

    return resp

@admin_blueprint.get("/api/logout")
def logout():
    resp = make_response(redirect(url_for("admin.login_page")))
    resp.set_cookie("access_token", "", expires=0)
    return resp
