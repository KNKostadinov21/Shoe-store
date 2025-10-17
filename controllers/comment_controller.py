from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import services.comment_service as comment_service
from models import Comment

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route("/add/<int:shoe_id>", methods=["POST"])
def add_comment(shoe_id):
    if "username" not in session:
        flash("Трябва да влезете в профила си, за да коментирате.", "danger")
        return redirect(url_for("auth.login"))

    comment_text = request.form.get("comment")
    parent_id = request.form.get("parent_id") or None

    if not comment_text:
        flash("Коментарът не може да е празен.", "danger")
        return redirect(url_for("shoe.view_shoe", shoe_id=shoe_id))

    user_id = session.get("user_id")  # увери се, че го пазиш при login
    comment_service.add_comment(comment_text, user_id, shoe_id, parent_id)
    flash("Коментарът е добавен!", "success")
    return redirect(url_for("shoe.view_shoe", shoe_id=shoe_id))
