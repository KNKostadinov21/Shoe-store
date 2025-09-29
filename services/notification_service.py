notifications = []
user_read = {}

def add_notification(message: str):
    notifications.append(message)

def get_unread_notifications(username: str):
    if username not in user_read:
        user_read[username] = set()

    unread = []
    for idx, note in enumerate(notifications):
        if idx not in user_read[username]:
            unread.append(note)
    return unread

def mark_all_read(username: str):
    if username not in user_read:
        user_read[username] = set()
    user_read[username].update(range(len(notifications)))
