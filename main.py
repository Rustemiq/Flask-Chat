from flask import Flask, render_template, make_response, jsonify, redirect
from flask_restful import Api
from flask_login import LoginManager, login_user, login_required, logout_user
from requests import post

from data.user_recources import UsersListResource
from data.chat_recources import ChatsListResource
from forms.user_register import RegisterForm
from forms.user_login import LoginForm
from forms.chat_creation import ChatCreationForm
from data.users import User
from data import db_session

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Wrong username or password",
                               form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/create_chat', methods=['GET', 'POST'])
def create_chat():
    form = ChatCreationForm()
    if form.validate_on_submit():
        if form.add_user.data:
            form.usernames.append_entry()
        elif form.delete_user.data:
            if form.usernames.__len__() > 1:
                form.usernames.pop_entry()
        elif form.confirm:
            db_sess = db_session.create_session()
            not_found_users = []
            for username in form.usernames:
                if not db_sess.query(User).filter(User.username == str(username.data['username'])).first():
                    not_found_users.append(username)
            if not_found_users:
                return render_template(
                    'chat_creation.html',
                    form=form,
                    not_found_users=not_found_users
                )
            post('http://127.0.0.1:8080/api/chats', json={
                'name': form.name.data,
                'members': form.usernames.data
                })
            return redirect('/')
    return render_template(
        'chat_creation.html',
        form=form, not_found_users = []
    )


if __name__ == '__main__':
    db_session.global_init('db/flask_chat.db')
    api.add_resource(UsersListResource, '/api/users')
    api.add_resource(ChatsListResource, '/api/chats')
    app.run(port='8080', host='127.0.0.1')
