from flask import Blueprint, render_template, request, redirect, url_for, flash
import services.catalog_service as catalog_service

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/manage")
def manage_shoes():
    shoes = catalog_service.get_all_shoes()
    return render_template("manage_shoes.html", shoes=shoes)

@admin_bp.route("/add", methods=["GET", "POST"])
def add_shoe():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        catalog_service.add_shoe(name, price)
        flash("Обувката е добавена!", "success")
        return redirect(url_for("admin.manage_shoes"))
    return render_template("add_shoe.html")

@admin_bp.route("/update/<int:shoe_id>", methods=["GET", "POST"])
def update_shoe(shoe_id):
    shoe = catalog_service.get_shoe_by_id(shoe_id)
    if not shoe:
        flash("Обувката не е намерена.", "error")
        return redirect(url_for("admin.manage_shoes"))

    if request.method == "POST":
        new_price = float(request.form["price"])
        catalog_service.update_shoe_price(shoe_id, new_price)
        flash("Цената е обновена!", "success")
        return redirect(url_for("admin.manage_shoes"))

    return render_template("update_shoe.html", shoe=shoe)

@admin_bp.route("/delete/<int:shoe_id>")
def delete_shoe(shoe_id):
    success = catalog_service.delete_shoe(shoe_id)
    if success:
        flash("Обувката е изтрита!", "info")
    else:
        flash("Грешка при изтриване.", "error")
    return redirect(url_for("admin.manage_shoes"))
