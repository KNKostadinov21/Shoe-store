from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask import request, redirect, url_for, flash, session, render_template, current_app
from werkzeug.utils import secure_filename
import os
from services import auth_service

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        success, message, user = auth_service.login(username, password)
        if success:
            session["username"] = user.username
            session["role"] = user.role
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


from flask import request, redirect, url_for, flash, session, render_template, current_app
from werkzeug.utils import secure_filename
import os
from services import auth_service

@auth_bp.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method == "POST":
        action = request.form.get("action")

        if action == "password":
            new_password = request.form["new_password"]
            if new_password:
                username = session["username"]
                success = auth_service.change_password(username, new_password)
                if success:
                    flash("Паролата е сменена!", "success")
                else:
                    flash("Грешка при смяната на паролата.", "danger")
            return redirect(url_for("auth.profile"))

        elif action == "image":
            file = request.files.get("image")
            if file and file.filename:
                filename = secure_filename(file.filename)
                upload_folder = os.path.join(current_app.root_path, "static/uploads")
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                flash("Снимката е качена! Админът ще я одобри.", "info")
            return redirect(url_for("auth.profile"))

    return render_template("profile.html")



@auth_bp.route("/admin/pending_images")
def pending_images():
    if session.get("role") != "admin":
        flash("Нямате достъп до тази страница.", "danger")
        return redirect(url_for("index"))

    upload_folder = os.path.join(current_app.root_path, "static/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    images = os.listdir(upload_folder)
    return render_template("admin_pending_images.html", images=images)



@auth_bp.route("/approve_image/<filename>")
def approve_image(filename):
    if session.get("role") != "admin":
        flash("Нямате права да одобрявате снимки.", "danger")
        return redirect(url_for("index"))

    upload_folder = os.path.join(current_app.root_path, "static/uploads")
    old_path = os.path.join(upload_folder, filename)
    approved_folder = os.path.join(upload_folder, "approved")
    os.makedirs(approved_folder, exist_ok=True)
    new_path = os.path.join(approved_folder, filename)
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        flash("Снимката е одобрена!", "success")
    return redirect(url_for("auth.pending_images"))

@auth_bp.route("/delete_image/<filename>")
def delete_image(filename):
    if session.get("role") != "admin":
        flash("Нямате права да триете снимки.", "danger")
        return redirect(url_for("index"))

    upload_folder = os.path.join(current_app.root_path, "static/uploads")
    path = os.path.join(upload_folder, filename)
    if os.path.exists(path):
        os.remove(path)
        flash("Снимката е изтрита.", "success")
    return redirect(url_for("auth.pending_images"))
