class Shoes:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.__price = price

    def get_price(self):
        return self.__price

    def set_price(self, price):
        if type(price) == int:
            self.__price = price

class SportsShoes(Shoes):
    def __init__(self, id : int, name : str, price : float, category="sport"):
        super().__init__(id, name, price)
        self.category = category

class OfficialShoes(Shoes):
    def __init__(self, id : int, name : str, price : float, category="official"):
        super().__init__(id, name, price)
        self.category = category

class EverydayShoes(Shoes):
    def __init__(self, id : int, name : str, price : float, category="everyday"):
        super().__init__(id, name, price)
        self.category = category

catalog = []

shoe1 = SportsShoes(1, "Nike", 100)
shoe2 = SportsShoes(2, "Fila", 120)
shoe3 = SportsShoes(3, "Puma", 200)
shoe4 = OfficialShoes(4, "Cafe Moda", 150)
shoe5 = EverydayShoes(5, "Easy street", 80)

catalog.extend([shoe1, shoe2, shoe3, shoe4, shoe5])

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
