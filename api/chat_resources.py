from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

from data.db_manager import DbManager
from data.models import db_session
from data.chats import Chat
from api.chat_parser import chat_parser

from flask import jsonify
from flask_restful import Resource, abort

from tools.response_if_no_access import response_if_not_member
from tools.response_if_not_found import response_if_not_found


class ChatsResource(Resource):
    @jwt_required()
    def post(self):
        args = chat_parser.parse_args()
        manager = DbManager()
        members_names = [member['username'] for member in args['members']]
        chat = manager.create_chat(name=args['name'], members_names=members_names)
        return jsonify({'id': chat.id})


class ChatResource(Resource):
    @jwt_required()
    def get(self, chat_id):
        manager = DbManager()
        chat = manager.get_chat(chat_id)
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        response_if_not_found(chat)
        response_if_not_found(user)
        response_if_not_member(user, chat)
        data = chat.to_dict(
            only=(
                'id',
                'name',
            ),
        )
        data['members'] = [member.id for member in chat.members]
        return jsonify({'chats': data})