from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User


def register_user(username, email, password, role="user"):
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()

    if existing_user:
        return False, "Потребител с това име или имейл вече съществува."

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password, role=role)
    db.session.add(new_user)
    db.session.commit()
    return True, "Регистрацията е успешна!"


def login(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return True, "Успешен вход!", user
    return False, "Грешно потребителско име или парола.", None


def get_all_users():
    return User.query.all()
