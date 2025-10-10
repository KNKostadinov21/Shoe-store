from flask import Blueprint, make_response, session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from io import BytesIO
from models import Shoe
from collections import Counter

pdf_bp = Blueprint('pdf_bp', __name__)

@pdf_bp.route('/export/cart')
def export_cart():
    raw_cart = session.get('cart', None)

    pdfmetrics.registerFont(UnicodeCIDFont('HeiseiMin-W3'))

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    if not raw_cart:
        p.setFont("HeiseiMin-W3", 14)
        p.drawString(100, height - 100, "Вашата количка е празна.")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=empty_cart.pdf'
        return response

    cart_counts = Counter()
    if isinstance(raw_cart, dict):
        for k, v in raw_cart.items():
            try:
                cart_counts[int(k)] = int(v)
            except Exception:
                continue
    elif isinstance(raw_cart, list):
        for entry in raw_cart:
            try:
                cart_counts[int(entry)] += 1
            except Exception:
                continue

    if not cart_counts:
        p.setFont("HeiseiMin-W3", 14)
        p.drawString(100, height - 100, "Вашата количка е празна.")
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=empty_cart.pdf'
        return response

    p.setFont("HeiseiMin-W3", 18)
    p.drawString(40, height - 50, "Експорт на количка — Shoe Store")
    p.setFont("HeiseiMin-W3", 10)
    user = session.get('username', 'Гост')
    p.drawString(40, height - 65, f"Потребител: {user}")

    y = height - 110
    p.setFont("HeiseiMin-W3", 11)
    p.drawString(40, y, "Име / Характеристики")
    p.drawString(300, y, "К-во")
    p.drawString(350, y, "Цена (бр.)")
    p.drawString(450, y, "Сума")
    y -= 6
    p.line(35, y, 560, y)
    y -= 20

    total_price = 0.0
    p.setFont("HeiseiMin-W3", 10)

    for shoe_id, qty in cart_counts.items():
        shoe = Shoe.query.get(shoe_id)
        if not shoe:
            continue

        name = getattr(shoe, "name", "Няма име")
        price = float(getattr(shoe, "price", 0.0))
        line_sum = price * int(qty)
        total_price += line_sum

        p.drawString(40, y, name)
        p.drawString(300, y, str(qty))
        p.drawString(350, y, f"{price:.2f}")
        p.drawString(450, y, f"{line_sum:.2f}")
        y -= 15

        material = getattr(shoe, "material", "-")
        size = getattr(shoe, "size", "-")
        color = getattr(shoe, "color", "-")
        category = getattr(shoe, "category", "-")
        type_ = getattr(shoe, "type", "-")

        features = f"Материал: {material}, Размер: {size}, Цвят: {color}, Категория: {category}, Тип: {type_}"
        p.drawString(50, y, features)
        y -= 20

        if y < 70:
            p.showPage()
            p.setFont("HeiseiMin-W3", 10)
            y = height - 50

    if y < 120:
        p.showPage()
        y = height - 100

    p.line(35, y - 6, 560, y - 6)
    p.setFont("HeiseiMin-W3", 12)
    p.drawString(350, y - 26, "Общо:")
    p.drawString(450, y - 26, f"{total_price:.2f}$")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    filename = "cart_export.pdf"
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'

    return response