from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    comments = db.relationship("Comment", backref="user", lazy=True, cascade="all, delete-orphan")
    cart_actions = db.relationship("CartAction", backref="user", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Shoe(db.Model):
    __tablename__ = "shoes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    material = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))

    comments = db.relationship("Comment", backref="shoe", lazy=True, cascade="all, delete-orphan")
    cart_actions = db.relationship("CartAction", backref="shoe", lazy=True, cascade="all, delete-orphan")

    __mapper_args__ = {
        "polymorphic_identity": "shoe",
        "polymorphic_on": type
    }

    def __repr__(self):
        return f"<Shoe {self.name} - {self.category}>"


class SportsShoes(Shoe):
    __mapper_args__ = {"polymorphic_identity": "sport"}

    def __init__(self, name, price, material, size, color):
        super().__init__(
            name=name,
            price=price,
            material=material,
            size=size,
            color=color,
            category="sport"
        )


class OfficialShoes(Shoe):
    __mapper_args__ = {"polymorphic_identity": "official"}

    def __init__(self, name, price, material, size, color):
        super().__init__(
            name=name,
            price=price,
            material=material,
            size=size,
            color=color,
            category="official"
        )


class EverydayShoes(Shoe):
    __mapper_args__ = {"polymorphic_identity": "everyday"}

    def __init__(self, name, price, material, size, color):
        super().__init__(
            name=name,
            price=price,
            material=material,
            size=size,
            color=color,
            category="everyday"
        )


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    shoe_model = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Order {self.id} - {self.name}>"


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    shoe_id = db.Column(db.Integer, db.ForeignKey("shoes.id"), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("comments.id"), nullable=True)

    replies = db.relationship(
        "Comment",
        backref=db.backref("parent", remote_side=[id]),
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Comment id={self.id}, user={self.user_id}, shoe={self.shoe_id}>"


class CartAction(db.Model):
    __tablename__ = "cart_actions"

    id = db.Column(db.Integer, primary_key=True)
    shoe_id = db.Column(db.Integer, db.ForeignKey("shoes.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<CartAction shoe={self.shoe_id}, user={self.user_id}, time={self.timestamp}>"
