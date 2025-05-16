from flask_restful import reqparse


chat_create_parser = reqparse.RequestParser()
chat_create_parser.add_argument("name", required=True)
chat_create_parser.add_argument("members", required=True, type=list, location="json")

chat_edit_parser = reqparse.RequestParser()
chat_edit_parser.add_argument("name", required=False)
chat_edit_parser.add_argument(
    "new_members", required=False, default=[], type=list, location="json"
)
chat_edit_parser.add_argument(
    "to_kick_members", required=False, default=[], type=list, location="json"
)
