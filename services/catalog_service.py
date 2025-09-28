class Shoes:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

catalog = []

shoe1 = Shoes(1, "Nike Air Zoom", 100)
shoe2 = Shoes(2, "Adidas Ultraboost", 120)
shoe3 = Shoes(3, "Puma RS-X", 200)

catalog.extend([shoe1, shoe2, shoe3])

def get_all_shoes():
    return list(catalog)

def get_shoe_by_id(shoe_id):
    for shoe in catalog:
        if shoe.id == shoe_id:
            return shoe
    return None

def add_shoe(name, price):
    new_id = max((shoe.id for shoe in catalog), default=0) + 1
    new_shoe = Shoes(new_id, name, price)
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
        shoe.price = new_price
        return True
    return False
