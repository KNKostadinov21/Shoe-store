from flask import Blueprint, render_template, request
import services.catalog_service as catalog_service

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