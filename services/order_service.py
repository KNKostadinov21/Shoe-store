orders = []

def add_order(name, address, email, shoe_model):
    new_order = {
        "id": len(orders) + 1,
        "name": name,
        "address": address,
        "email": email,
        "shoe_model": shoe_model
    }
    orders.append(new_order)
    return new_order

def get_all_orders():
    return orders
