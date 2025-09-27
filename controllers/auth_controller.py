from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import services.auth_service as auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success, message, user = auth_service.login(username, password)
        if success:
            session["username"] = user["username"]
            session["role"] = user.get("role", "user")
            flash(message, "success")
            return redirect(url_for("index"))
        else:
            flash(message, "error")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        success, message = auth_service.register_user(username, email, password)
        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))
        else:
            flash(message, "error")

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("role", None)
    session.pop("cart", None)
    flash("Излязохте от профила.", "info")
    return redirect(url_for("index"))
