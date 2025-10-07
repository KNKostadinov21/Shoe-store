from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    def __repr__(self):
        return f"<User {self.username}>"


class Shoe(db.Model):
    __tablename__ = "shoes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    type = db.Column(db.String(50))
    __mapper_args__ = {
        "polymorphic_identity": "shoe",
        "polymorphic_on": type
    }

    def __repr__(self):
        return f"<Shoe {self.name} - {self.category}>"


class SportsShoes(Shoe):
    __mapper_args__ = {"polymorphic_identity": "sport"}

    def __init__(self, name, price):
        super().__init__(name=name, price=price, category="sport")


class OfficialShoes(Shoe):
    __mapper_args__ = {"polymorphic_identity": "official"}

    def __init__(self, name, price):
        super().__init__(name=name, price=price, category="official")


class EverydayShoes(Shoe):
    __mapper_args__ = {"polymorphic_identity": "everyday"}

    def __init__(self, name, price):
        super().__init__(name=name, price=price, category="everyday")


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    shoe_model = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Order {self.id} - {self.name}>"