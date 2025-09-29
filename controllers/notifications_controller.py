from flask import Blueprint, render_template, session, redirect, url_for
import services.notification_service as notification_service

notifications_bp = Blueprint("notifications", __name__, url_prefix="/notifications")

@notifications_bp.route("/")
def view_notifications():
    username = session.get("username")
    if not username:
        return redirect(url_for("auth.login"))

    notes = notification_service.get_unread_notifications(username)
    notification_service.mark_all_read(username)

    return render_template("notifications.html", notifications=notes)