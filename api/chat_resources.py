from http import HTTPStatus

from flask_jwt_extended import jwt_required, get_jwt_identity

from data.db_manager import DbManager
from api.chat_parser import chat_create_parser, chat_edit_parser

from flask import jsonify
from flask_restful import Resource

from tools.response_if_no_access import response_if_not_member
from tools.response_if_not_found import response_if_not_found


class ChatsResource(Resource):
    @jwt_required()
    def post(self):
        args = chat_create_parser.parse_args()
        manager = DbManager()
        members = args["members"]

        for member_name in members:
            member = manager.get_user_by_name(member_name)
            response_if_not_found(member)

        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        members.append(user.username)
        chat = manager.create_chat(name=args["name"], members_names=members)
        return jsonify({"id": chat.id})

    @jwt_required()
    def get(self):
        manager = DbManager()
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        chats = user.chats
        return jsonify({"chats": [chat.to_dict(only=("id", "name")) for chat in chats]})


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
                "id",
                "name",
            ),
        )
        data["members"] = [member.id for member in chat.members]
        data["messages"] = [message.id for message in chat.messages]
        return jsonify({"chats": data})

    @jwt_required()
    def put(self, chat_id):
        args = chat_edit_parser.parse_args()
        manager = DbManager()
        chat = manager.get_chat(chat_id)
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        response_if_not_found(chat)
        response_if_not_found(user)
        response_if_not_member(user, chat)
        for username in args["to_kick_members"]:
            to_kick_user = manager.get_user_by_name(username)
            response_if_not_found(to_kick_user)
            response_if_not_member(to_kick_user, chat)
            chat.members.remove(to_kick_user)
        name = args.get("name", chat.name)
        new_members = args["new_members"]
        manager.edit_chat(chat_id, name=name, new_members=new_members)
        return jsonify({"success": HTTPStatus.OK})

    @jwt_required()
    def delete(self, chat_id):
        manager = DbManager()
        chat = manager.get_chat(chat_id)
        user_id = int(get_jwt_identity())
        user = manager.get_user(user_id)
        response_if_not_found(chat)
        response_if_not_found(user)
        response_if_not_member(user, chat)
        manager.delete_chat(chat.id)

        return jsonify({"success": HTTPStatus.OK})
