from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_login import LoginManager
from flask_uploads import configure_uploads, UploadSet

from api.user_resources import UsersListResource, UsersResource
from api.chat_resources import ChatsResource, ChatResource
from blueprints import users_blueprint, chats_blueprint, pages_blueprint, api_login
from data.db_manager import DbManager
from data.models import db_session
from decouple import config

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = config('secret_key', default='default_secretkey')
app.config['UPLOADED_MESSAGES_DEST'] = 'media/message_files'
app.config['UPLOADED_MESSAGES_URL'] = 'media/message_files/'
app.config['UPLOADED_MESSAGES_ALLOW'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config["JWT_SECRET_KEY"] = config('jwt_secret_key', default='default_secretkey')
messages = UploadSet('messages')
configure_uploads(app, messages)

login_manager = LoginManager()
login_manager.init_app(app)

jwt = JWTManager(app)


@login_manager.user_loader
def load_user(user_id):
    manager = DbManager()
    return manager.get_user(user_id)


if __name__ == '__main__':
    db_session.global_init('db/flask_chat.db')
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(UsersResource, '/api/users/<int:user_id>')
    api.add_resource(ChatsResource, '/api/chats')
    api.add_resource(ChatResource, '/api/chats/<int:chat_id>')
    app.register_blueprint(users_blueprint.blueprint)
    app.register_blueprint(chats_blueprint.blueprint)
    app.register_blueprint(pages_blueprint.blueprint)
    app.register_blueprint(api_login.blueprint)
    app.run(port='8080', host='127.0.0.1')
