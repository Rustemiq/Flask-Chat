from flask import Flask, render_template, make_response, jsonify
from flask_restful import Api
from requests import post

from data.user_recources import UsersListResource
from forms.user_register import RegisterForm
from data.users import User
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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                'register.html',
                title='Registration',
                form=form,
                message='Passwords do not match'
            )
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.username == form.username.data).first():
            return render_template(
                'register.html',
                title='Registration',
                form=form,
                message='Username is taken'
            )
        post('http://127.0.0.1:8080/api/users', json={
            'nickname': form.nickname.data,
            'username': form.username.data,
            'birth_date': str(form.birth_date.data),
            'password': form.password.data})
    return render_template('register.html', title='Registration', form=form)


if __name__ == '__main__':
    db_session.global_init('db/flask_chat.db')
    api.add_resource(UsersListResource, '/api/users')
    app.run(port='8080', host='127.0.0.1')
