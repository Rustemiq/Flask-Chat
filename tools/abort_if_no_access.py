from http import HTTPStatus
from flask import abort


def abort_if_not_member(user, chat):
    if user not in chat.members:
        abort(HTTPStatus.FORBIDDEN)


def abort_if_not_msg_author(user, message):
    if user != message.author:
        abort(HTTPStatus.FORBIDDEN)


def abort_if_not_concrete_user(cur_user, user):
    if cur_user != user:
        abort(HTTPStatus.FORBIDDEN)


def abort_if_authenticated(user):
    if user.is_authenticated:
        abort(HTTPStatus.CONFLICT)

