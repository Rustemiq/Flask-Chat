from flask import Flask, make_response, jsonify
from flask_restful import Api
from flask_login import LoginManager

from api.user_resources import UsersListResource, UsersResource
from api.chat_resources import ChatsListResource, ChatsResource
from blueprints import users_blueprint, chats_blueprint, pages_blueprint, errorhandlers_blueprint
from data.db_manager import DbManager
from data.models import db_session
from decouple import config

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = config('secret_key', default='default_secretkey')
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    manager = DbManager()
    return manager.get_user(user_id)


if __name__ == '__main__':
    db_session.global_init('db/flask_chat.db')
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
    api.add_resource(ChatsListResource, '/api/chats')
    api.add_resource(ChatsResource, '/api/chats/<int:chat_id>')
    app.register_blueprint(users_blueprint.blueprint)
    app.register_blueprint(chats_blueprint.blueprint)
    app.register_blueprint(pages_blueprint.blueprint)
    app.register_blueprint(errorhandlers_blueprint.blueprint)
    app.run(port='8080', host='127.0.0.1')
