from flask import Blueprint, session, render_template, redirect, url_for, flash
import services.catalog_service as catalog_service

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route("/add/<int:shoe_id>", methods=["POST"])
def add_to_cart(shoe_id):
    shoe = catalog_service.get_shoe_by_id(shoe_id)
    if not shoe:
        flash("Обувката не е намерена.", "error")
        return redirect(url_for("catalog.catalog_list"))

    cart = session.get("cart", [])
    cart.append(shoe)
    session["cart"] = cart
    flash(f"{shoe['name']} е добавена в количката!", "success")
    return redirect(url_for("catalog.catalog_list"))

@cart_bp.route("/")
def view_cart():
    cart = session.get("cart", [])
    total = sum(item["price"] for item in cart)
    return render_template("cart.html", cart=cart, total=total)

@cart_bp.route("/remove/<int:shoe_id>")
def remove_from_cart(shoe_id):
    cart = session.get("cart", [])
    cart = [item for item in cart if item["id"] != shoe_id]
    session["cart"] = cart
    flash("Обувката е премахната от количката.", "info")
    return redirect(url_for("cart.view_cart"))
