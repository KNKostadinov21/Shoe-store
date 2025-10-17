from models import db, Comment

def add_comment(comment_text, user_id, shoe_id, parent_id=None):
    comment = Comment(
        comment=comment_text,
        user_id=user_id,
        shoe_id=shoe_id,
        parent_id=parent_id
    )
    db.session.add(comment)
    db.session.commit()
    return comment


def get_comments_for_shoe(shoe_id):
    return Comment.query.filter_by(shoe_id=shoe_id, parent_id=None).all()

def get_comment_replies(comment_id):
    return Comment.query.filter_by(parent_id=comment_id).all()