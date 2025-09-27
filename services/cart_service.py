def get_cart(session):
    if "cart" not in session:
        session["cart"] = []
    return session["cart"]

def add_to_cart(session, shoe):
    cart = get_cart(session)
    cart.append({"id": shoe["id"], "name": shoe["name"], "price": shoe["price"]})
    session.modified = True

def remove_from_cart(session, shoe_id):
    cart = get_cart(session)
    for i, item in enumerate(cart):
        if item.get("id") == shoe_id:
            cart.pop(i)
            session.modified = True
            return True
    return False