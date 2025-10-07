from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.admin_controller import admin_bp
from controllers.order_controller import order_bp

from models import db, User, Shoe, SportsShoes, OfficialShoes, EverydayShoes, Order


app = Flask(__name__)
app.secret_key = "supersecret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shoe_store.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(order_bp)


@app.route("/")
def index():
    return render_template("index.html")


@app.before_request
def restrict_admin_pages():
    if request.path.startswith("/admin"):
        if session.get("role") != "admin":
            flash("Нямате достъп до админ панела.", "error")
            return redirect(url_for("index"))


@app.before_request
def setup_database():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        hashed_password = generate_password_hash("admin123")
        admin_user = User(username="admin", email="admin@admin.com", password=hashed_password, role="admin")
        db.session.add(admin_user)
        db.session.commit()

    if not Shoe.query.first():
        demo_shoes = [
            SportsShoes(name="Nike", price=100),
            SportsShoes(name="Fila", price=120),
            SportsShoes(name="Puma", price=200),
            OfficialShoes(name="Cafe Moda", price=150),
            EverydayShoes(name="Easy Street", price=80)
        ]
        db.session.add_all(demo_shoes)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)
