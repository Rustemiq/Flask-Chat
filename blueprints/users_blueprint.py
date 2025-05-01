from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_user, login_required, logout_user
from requests import post

from forms.user_login import LoginForm
from forms.user_register import RegisterForm
from data.models import db_session
from data.users import User

blueprint = Blueprint(
    'users_function',
    __name__,
    template_folder='templates'
)


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/')
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
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
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


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")