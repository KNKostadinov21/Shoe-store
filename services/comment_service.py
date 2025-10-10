from models import db, Comment


def add_comment(message):
    comment = Comment(comment=message)
    db.session.add(comment)
    db.session.commit()
    return comment