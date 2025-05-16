from http import HTTPStatus
from flask_restful import abort


def response_if_not_member(user, chat):
    if user not in chat.members:
        abort(HTTPStatus.FORBIDDEN, message=f"Permission denied")


def response_if_not_msg_author(user, message):
    if user != message.author:
        abort(HTTPStatus.FORBIDDEN, message=f"Permission denied")


def response_if_not_concrete_user(cur_user_id, user_id):
    if cur_user_id != user_id:
        abort(HTTPStatus.FORBIDDEN, message=f"Permission denied")
