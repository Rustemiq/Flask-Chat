from tools.response_if_not_found import response_if_not_found

from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

from data.db_manager import DbManager
from api.message_parser import message_create_parser, message_edit_parser

from flask import jsonify
from flask_restful import Resource

from tools.response_if_no_access import response_if_not_msg_author, \
    response_if_not_member


class MessagesResource(Resource):
    @jwt_required()
    def post(self):
        args = message_create_parser.parse_args()
        manager = DbManager()
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        chat = manager.get_chat(args['chat_id'])
        response_if_not_found(chat)
        response_if_not_member(user, chat)
        message = manager.create_message(chat.id, user.id, text=args['text'])
        return jsonify({'id': message.id})

    @jwt_required()
    def get(self):
        manager = DbManager()
        user_id = get_jwt_identity()
        user = manager.get_user(user_id)
        messages = []
        for chat in user.chats:
            messages.extend(chat.messages)
        return jsonify({'messages': [message.to_dict(only=('id', 'text', 'author_id', 'chat_id')) for message in messages]})


class MessageResource(Resource):
    @jwt_required()
    def get(self, message_id):
        manager = DbManager()
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        message = manager.get_message(message_id)
        response_if_not_found(message)
        response_if_not_member(user, message.chat)
        data = message.to_dict(
            only=(
                'id',
                'text',
                'chat_id',
                'author_id'
            ),
        )
        data['files'] = [file.id for file in message.files]
        return jsonify({'messages': data})

    @jwt_required()
    def put(self, message_id):
        args = message_edit_parser.parse_args()
        manager = DbManager()
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        message = manager.get_message(message_id)
        response_if_not_found(message)
        response_if_not_msg_author(user, message)
        text = args['text'] if args['text'] is not None else message.text
        manager.edit_message(message_id, text)
        return jsonify({'success': HTTPStatus.OK})

    @jwt_required()
    def delete(self, message_id):
        manager = DbManager()
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        message = manager.get_message(message_id)
        response_if_not_found(message)
        response_if_not_msg_author(user, message)
        manager.delete_message(message.id)
        return jsonify({'success': HTTPStatus.OK})