from data.db_manager import DbManager
from data.models import db_session
from data.chats import Chat
from api.chat_parser import chat_parser

from flask import jsonify
from flask_restful import Resource, abort


def abort_if_chat_not_found(chat_id):
    session = db_session.create_session()
    chat = session.query(Chat).get(chat_id)
    if not chat:
        abort(404, message=f"Chat {chat_id} not found")


class ChatsListResource(Resource):
    def post(self):
        args = chat_parser.parse_args()
        manager = DbManager()
        members_names = [member['username'] for member in args['members']]
        chat = manager.create_chat(name=args['name'], members_names=members_names)
        return jsonify({'id': chat.id})


class ChatsResource(Resource):
    def get(self, chat_id):
        abort_if_chat_not_found(chat_id)
        manager = DbManager()
        chat = manager.get_chat(chat_id)
        data = chat.to_dict(
            only=(
                'id',
                'name',
            ),
        )
        data['members'] = [member.id for member in chat.members]
        return jsonify({'chats': data})