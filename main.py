from flask import Flask, render_template, make_response, jsonify
from flask_restful import Api

from data.user_recources import UsersListResource
from data import db_session

app = Flask(__name__)
api = Api(app)
with open('secret_key/secret_key.txt', 'r') as f:
    app.config['SECRET_KEY'] = f.read()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('base.html')


if __name__ == '__main__':
    db_session.global_init('db/flask_chat.db')
    api.add_resource(UsersListResource, '/api/users')
    app.run(port='8080', host='127.0.0.1')
