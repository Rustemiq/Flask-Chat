from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

from data.db_manager import DbManager
from api.user_parser import user_create_parser, user_edit_parser

from flask import jsonify
from flask_restful import Resource, abort

from tools.response_if_invalid_date import response_if_invalid_date
from tools.response_if_no_access import response_if_not_concrete_user


class UsersResource(Resource):
    def post(self):
        args = user_create_parser.parse_args()
        manager = DbManager()
        if manager.get_user_by_name(args["username"]):
            abort(HTTPStatus.CONFLICT, message="Username is taken")
        response_if_invalid_date(args["birth_date"])
        user = manager.create_user(*args.values())
        return jsonify({"id": user.id})

    def get(self):
        manager = DbManager()
        users = manager.get_all_users()
        return jsonify(
            {"users": [user.to_dict(only=("id", "username")) for user in users]}
        )


class UserResource(Resource):
    def get(self, user_id):
        manager = DbManager()
        user = manager.get_user(user_id)
        data = user.to_dict(
            only=("id", "nickname", "username", "birth_date"),
        )
        data["chats"] = [chat.id for chat in user.chats]
        return jsonify({"users": data})

    @jwt_required()
    def put(self, user_id):
        args = user_edit_parser.parse_args()
        manager = DbManager()
        cur_user_id = int(get_jwt_identity())
        response_if_not_concrete_user(cur_user_id, user_id)
        user = manager.get_user(user_id)
        args = dict(args)
        username = args["username"] if args["username"] is not None else user.username
        nickname = args["nickname"] if args["nickname"] is not None else user.nickname
        birth_date = (
            args["birth_date"] if args["birth_date"] is not None else user.birth_date
        )
        response_if_invalid_date(birth_date)
        manager.edit_user(
            user_id, nickname=nickname, username=username, birth_date=birth_date
        )
        if args["password"] is not None:
            manager.edit_user(user_id, password=args["password"])
        return jsonify({"success": HTTPStatus.OK})

    @jwt_required()
    def delete(self, user_id):
        manager = DbManager()
        cur_user_id = int(get_jwt_identity())
        response_if_not_concrete_user(cur_user_id, user_id)
        manager.delete_user(user_id)
        return jsonify({"success": HTTPStatus.OK})
