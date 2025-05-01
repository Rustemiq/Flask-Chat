from flask import Flask, make_response, jsonify
from flask_restful import Api
from flask_login import LoginManager

from api.user_resources import UsersListResource, UsersResource
from api.chat_resources import ChatsListResource, ChatsResource
from blueprints import users_blueprint, chats_blueprint, pages_blueprint
from data.users import User
from data.models import db_session

app = Flask(__name__)
api = Api(app)
with open('secret_key/secret_key.txt', 'r') as f:
    app.config['SECRET_KEY'] = f.read()
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    db_session.global_init('db/flask_chat.db')
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
    api.add_resource(ChatsListResource, '/api/chats')
    api.add_resource(ChatsResource, '/api/chats/<int:chat_id>')
    app.register_blueprint(users_blueprint.blueprint)
    app.register_blueprint(chats_blueprint.blueprint)
    app.register_blueprint(pages_blueprint.blueprint)
    app.run(port='8080', host='127.0.0.1')
