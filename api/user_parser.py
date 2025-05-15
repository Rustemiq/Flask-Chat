from flask_restful import reqparse


user_create_parser = reqparse.RequestParser()
user_create_parser.add_argument('nickname', required=True)
user_create_parser.add_argument('username', required=True)
user_create_parser.add_argument('birth_date', required=True)
user_create_parser.add_argument('password', required=True)

user_edit_parser = reqparse.RequestParser()
user_edit_parser.add_argument('nickname', required=False)
user_edit_parser.add_argument('username', required=False)
user_edit_parser.add_argument('birth_date', required=False)
user_edit_parser.add_argument('password', required=False)

