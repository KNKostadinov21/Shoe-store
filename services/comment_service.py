from models import db, Comment


def add_comment(message):
    comment = Comment(comment=message)
    db.session.add(message)
    db.session.commit()
    return comment