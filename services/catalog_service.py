from models import db, Shoe, SportsShoes, OfficialShoes, EverydayShoes


def get_all_shoes():
    return Shoe.query.all()


def get_shoe_by_id(shoe_id):
    return Shoe.query.get(shoe_id)


def add_shoe(name, price, category):
    if category == "sport":
        new_shoe = SportsShoes(name=name, price=price)
    elif category == "official":
        new_shoe = OfficialShoes(name=name, price=price)
    elif category == "everyday":
        new_shoe = EverydayShoes(name=name, price=price)
    else:
        new_shoe = Shoe(name=name, price=price, category=category)

    db.session.add(new_shoe)
    db.session.commit()
    return new_shoe


def delete_shoe(shoe_id):
    shoe = get_shoe_by_id(shoe_id)
    if shoe:
        db.session.delete(shoe)
        db.session.commit()
        return True
    return False


def update_shoe_price(shoe_id, new_price):
    shoe = get_shoe_by_id(shoe_id)
    if shoe:
        shoe.price = new_price
        db.session.commit()
        return True
    return False
