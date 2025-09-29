from flask import Blueprint, render_template, request
import services.catalog_service as catalog_service

catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/')
def catalog_list():
    query = request.args.get("q", "").lower()
    min_price = request.args.get("min_price", type=float, default=0)
    max_price = request.args.get("max_price", type=float, default=9999)
    category = request.args.get("category", "").lower()

    shoes = catalog_service.get_all_shoes()

    if query:
        shoes = [s for s in shoes if query in s.name.lower()]

    shoes = [s for s in shoes if min_price <= s.price <= max_price]

    if category:
        shoes = [s for s in shoes if s.category.lower() == category]

    return render_template(
        "catalog.html",
        shoes=shoes,
        query=query,
        min_price=min_price,
        max_price=max_price,
        category=category
    )