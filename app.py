from flask import Flask, render_template, session, request, redirect, url_for, flash
from controllers.auth_controller import auth_bp
from controllers.catalog_controller import catalog_bp
from controllers.cart_controller import cart_bp
from controllers.admin_controller import admin_bp
from controllers.order_controller import order_bp
from controllers.notifications_controller import notifications_bp
import services.notification_service as notification_service

app = Flask(__name__)
app.secret_key = "supersecret"

app.register_blueprint(auth_bp)
app.register_blueprint(catalog_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(order_bp)
app.register_blueprint(notifications_bp)

@app.route("/")
def index():
    return render_template("index.html")

@app.before_request
def restrict_admin_pages():
    if request.path.startswith("/admin"):
        if session.get("role") != "admin":
            flash("Нямате достъп до админ панела.", "error")
            return redirect(url_for("index"))

@app.context_processor
def inject_notifications():
    username = session.get("username")
    if username:
        unread = notification_service.get_unread_notifications(username)
        return {"notification_count": len(unread)}
    return {"notification_count": 0}

if __name__ == "__main__":
    app.run(debug=True)