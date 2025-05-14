from http import HTTPStatus
from flask import abort


def abort_if_not_found(obj):
    if obj is None:
        abort(HTTPStatus.NOT_FOUND)