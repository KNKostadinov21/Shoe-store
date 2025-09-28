class User:
    def __init__(self, username, email, password, role):
        self.username = username
        self.email = email
        self.password = password
        self.role = role

users = []

admin = User("admin", "admin@admin.com", "admin123", "admin")
user1 = User("user1", "user1@user.com", "user1", "user")
user2 = User("user2", "user2@user.com", "user2", "user")

users.append(admin)
users.append(user1)
users.append(user2)

def register_user(username, email, password):
    if any(u.username == username for u in users):
        return False, "Потребителското име вече съществува."

    new_user = User(username, email, password, "user")

    users.append(new_user)
    return True, "Успешна регистрация!"

def login(username, password):
    user = next((u for u in users if u.username == username and u.password == password), None)
    if user:
        return True, "Успешен вход!", user
    return False, "Грешно потребителско име или парола.", None

def get_all_users():
    return users