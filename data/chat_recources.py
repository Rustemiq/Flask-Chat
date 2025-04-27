from data import db_session
from data.chats import Chat
from data.users import User
from data.chat_parser import chat_parser

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
        session = db_session.create_session()
        chat = Chat(
            name=args['name'],
        )
        for user_data in args['members']:
            user = session.query(User).filter(User.username == user_data['username']).first()
            if not user:
                abort(404, message=f'User {user_data['username']} not found')
            chat.members.append(user)
        session.add(chat)
        session.commit()
        return jsonify({'id': chat.id})