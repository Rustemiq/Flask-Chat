from data.db_manager import DbManager
from data.models import db_session
from data.users import User
from api.user_parser import user_parser

from flask import abort, jsonify
from flask_restful import Resource


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UsersListResource(Resource):
    def post(self):
        args = user_parser.parse_args()
        manager = DbManager()
        user = manager.create_user(*args.values())
        return jsonify({'id': user.id})


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        manager = DbManager()
        user = manager.get_user(user_id)
        data = user.to_dict(
            only=(
                'id',
                'nickname',
                'username',
                'birth_date'
            ),
        )
        data['chats'] = [chat.id for chat in user.chats]
        return jsonify({'users': data})