from flask import Blueprint, render_template, request, redirect, url_for, flash
import services.order_service as order_service

order_bp = Blueprint("order", __name__, url_prefix="/order")

@order_bp.route("/create", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        email = request.form["email"]
        shoe_model = request.form["shoe_model"]

        order_service.add_order(name, address, email, shoe_model)
        flash("Поръчката е направена успешно!", "success")
        return redirect(url_for("index"))

    return render_template("create_order.html")

@order_bp.route("/list")
def list_orders():
    orders = order_service.get_all_orders()
    return render_template("list_orders.html", orders=orders)
