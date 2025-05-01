from flask_restful import reqparse


user_parser = reqparse.RequestParser()
user_parser.add_argument('nickname', required=True)
user_parser.add_argument('username', required=True)
user_parser.add_argument('birth_date', required=True)
user_parser.add_argument('password', required=True)
