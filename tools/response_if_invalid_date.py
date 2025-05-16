import datetime
from http import HTTPStatus

from flask_restful import abort


def is_valid_date(date_string):
    try:
        datetime.datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def response_if_invalid_date(date):
    if not is_valid_date(date):
        abort(HTTPStatus.BAD_REQUEST, message="Invalid date")
