from flask_restful import reqparse


message_create_parser = reqparse.RequestParser()
message_create_parser.add_argument('text', required=True)
message_create_parser.add_argument('chat_id', required=True, type=int)

message_edit_parser = reqparse.RequestParser()
message_edit_parser.add_argument('text', required=False)