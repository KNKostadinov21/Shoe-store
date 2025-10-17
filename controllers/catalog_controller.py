from flask import Blueprint, render_template, request
import services.catalog_service as catalog_service
from flask import session, flash, redirect, url_for
import services.comment_service as comment_service
from models import db, Shoe, Comment, User
import datetime


catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/')
def catalog_list():
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    shoes = catalog_service.get_all_shoes()

    if query:
        shoes = [s for s in shoes if query in s.name.lower()]

    if category:
        shoes = [s for s in shoes if getattr(s, "category", "") == category]

    if min_price is not None:
        shoes = [s for s in shoes if s.price >= min_price]
    if max_price is not None:
        shoes = [s for s in shoes if s.price <= max_price]

    return render_template(
        "catalog.html",
        shoes=shoes,
        query=query,
        category=category,
        min_price=min_price,
        max_price=max_price
    )

@catalog_bp.route("/<int:shoe_id>", methods=["GET", "POST"])
def shoe_details(shoe_id):
    shoe = Shoe.query.get_or_404(shoe_id)

    if request.method == "POST":
        if "username" not in session:
            flash("Трябва да сте влезли, за да коментирате.", "danger")
            return redirect(url_for("auth.login"))

        message = request.form.get("comment")
        parent_id = request.form.get("parent_id")  # ако е отговор
        username = session["username"]
        user = User.query.filter_by(username=username).first()

        comment = Comment(
            comment=message,
            user_id=user.id,
            shoe_id=shoe.id,
            parent_id=parent_id if parent_id else None
        )

        db.session.add(comment)
        db.session.commit()
        flash("Коментарът е добавен успешно!", "success")
        return redirect(url_for("catalog.shoe_details", shoe_id=shoe_id))

    comments = Comment.query.filter_by(shoe_id=shoe_id, parent_id=None).all()

    return render_template("shoe_details.html", shoe=shoe, comments=comments)