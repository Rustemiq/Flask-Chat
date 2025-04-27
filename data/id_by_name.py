from data.users import User
from flask_restful import abort


def id_by_name(username, db_sess):
    user = db_sess.query(User).filter(User.username == username).first()
    if not user:
        abort(404, message=f'User {username} not found')
    return user.id