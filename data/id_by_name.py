from data.users import User


def id_by_name(username, db_sess):
    user = db_sess.query(User).filter(User.username == username).first()
    return user.id