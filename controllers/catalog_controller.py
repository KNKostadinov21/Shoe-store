from flask import Blueprint, render_template, request
import services.catalog_service as catalog_service

catalog_bp = Blueprint('catalog', __name__, url_prefix='/catalog')

@catalog_bp.route('/')
def catalog_list():
    query = request.args.get("q", "").lower()
    shoes = catalog_service.get_all_shoes()

    if query:
        shoes = [s for s in shoes if query in s.name.lower()]

    return render_template("catalog.html", shoes=shoes, query=query)
