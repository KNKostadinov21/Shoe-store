def get_cart(session):
    if "cart" not in session:
        session["cart"] = []
    return session["cart"]

def add_to_cart(session, shoe):
    cart = get_cart(session)
    cart.append(shoe.id)
    session.modified = True

def remove_from_cart(session, shoe_id):
    cart = get_cart(session)
    if shoe_id in cart:
        cart.remove(shoe_id)
        session.modified = True
        return True
    return False