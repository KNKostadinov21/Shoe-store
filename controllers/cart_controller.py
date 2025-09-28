from flask import Blueprint, session, render_template, redirect, url_for, flash
import services.catalog_service as catalog_service
import services.cart_service as cart_service

cart_bp = Blueprint("cart", __name__, url_prefix="/cart")

@cart_bp.route("/add/<int:shoe_id>", methods=["POST"])
def add_to_cart(shoe_id):
    shoe = catalog_service.get_shoe_by_id(shoe_id)
    if not shoe:
        flash("Обувката не е намерена.", "error")
        return redirect(url_for("catalog.catalog_list"))

    cart_service.add_to_cart(session, shoe)
    flash(f"{shoe.name} е добавена в количката!", "success")
    return redirect(url_for("catalog.catalog_list"))

@cart_bp.route("/")
def view_cart():
    cart_ids = cart_service.get_cart(session)
    cart_items = [catalog_service.get_shoe_by_id(i) for i in cart_ids if catalog_service.get_shoe_by_id(i)]
    total = sum(item.price for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@cart_bp.route("/remove/<int:shoe_id>")
def remove_from_cart(shoe_id):
    success = cart_service.remove_from_cart(session, shoe_id)
    if success:
        flash("Обувката е премахната от количката.", "info")
    else:
        flash("Грешка при премахване.", "error")
    return redirect(url_for("cart.view_cart"))
