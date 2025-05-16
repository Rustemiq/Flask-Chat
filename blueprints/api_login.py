from http import HTTPStatus

from flask import make_response, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from flask_restful import reqparse

from data.db_manager import DbManager

blueprint = Blueprint("api_login", __name__, template_folder="templates")


login_parser = reqparse.RequestParser()
login_parser.add_argument("username", required=True)
login_parser.add_argument("password", required=True)


@blueprint.route("/api/users/login", methods=["POST"])
def login():
    args = login_parser.parse_args()
    username = args["username"]
    password = args["password"]
    manager = DbManager()
    user = manager.get_user_by_name(username)
    if not user or not user.check_password(password):
        return make_response(
            jsonify({"error": "Wrong username or password"}), HTTPStatus.OK
        )
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"message": "Success", "access_token": access_token})
