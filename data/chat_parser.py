from flask_restful import reqparse


chat_parser = reqparse.RequestParser()
chat_parser.add_argument('name', required=True)
chat_parser.add_argument('members', required=True, type=list, location='json')
