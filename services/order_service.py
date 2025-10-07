from models import db, Order


def add_order(name, address, email, shoe_model):
    new_order = Order(
        name=name,
        address=address,
        email=email,
        shoe_model=shoe_model
    )
    db.session.add(new_order)
    db.session.commit()
    return new_order


def get_all_orders():
    return Order.query.all()
