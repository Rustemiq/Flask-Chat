from http import HTTPStatus

from flask_restful import abort


def response_if_not_found(obj):
    if obj is None:
        abort(HTTPStatus.NOT_FOUND, message='Not found')