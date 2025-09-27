users = [
    {"username": "admin", "email": "admin@admin.com", "password": "admin123", "role": "admin"},
    {"username": "user1", "email": "user1@user.com", "password": "user1", "role": "user"},
    {"username": "user2", "email": "user2@user.com", "password": "user2", "role": "user"},
]

def register_user(username, email, password):
    if any(u["username"] == username for u in users):
        return False, "Потребителското име вече съществува."

    new_user = {
        "username": username,
        "email": email,
        "password": password,
        "role": "user"
    }

    users.append(new_user)
    return True, "Успешна регистрация!"

def login(username, password):
    user = next((u for u in users if u["username"] == username and u["password"] == password), None)
    if user:
        return True, "Успешен вход!", user
    return False, "Грешно потребителско име или парола.", None

def get_all_users():
    return users
