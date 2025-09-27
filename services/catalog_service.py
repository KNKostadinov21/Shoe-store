catalog = [
    {"id": 1, "name": "Nike Air Zoom", "price": 100},
    {"id": 2, "name": "Adidas Ultraboost", "price": 120},
    {"id": 3, "name": "Puma RS-X", "price": 200},
]

def get_all_shoes():
    return list(catalog)

def get_shoe_by_id(shoe_id):
    for shoe in catalog:
        if shoe["id"] == shoe_id:
            return shoe
    return None

def add_shoe(name, price):
    new_id = max((shoe["id"] for shoe in catalog), default=0) + 1
    new_shoe = {"id": new_id, "name": name, "price": price}
    catalog.append(new_shoe)
    return new_shoe

def delete_shoe(shoe_id):
    shoe = get_shoe_by_id(shoe_id)
    if shoe:
        catalog.remove(shoe)
        return True
    return False

def update_shoe_price(shoe_id, new_price):
    shoe = get_shoe_by_id(shoe_id)
    if shoe:
        shoe["price"] = new_price
        return True
    return False