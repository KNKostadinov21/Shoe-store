from flask import Blueprint, render_template, request, flash, redirect, url_for
import services.comment_service as comment_service

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route("/add", methods=["GET", "POST"])
def add_comment():
    if request.method == "POST":
        comment = request.form["comment"]

        comment_service.add_comment(comment)
        flash("Коментарът е добавен успешно!", "success")
        return redirect(url_for("index"))

    return render_template("comment.html")