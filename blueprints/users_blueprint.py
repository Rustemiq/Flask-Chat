from flask import Blueprint, redirect, render_template
from flask_login import current_user, login_user, login_required, logout_user

from data.db_manager import DbManager
from forms.user_login import LoginForm
from forms.user_register import RegisterForm

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
                form=form,
                message='Passwords do not match'
            )
        manager = DbManager()
        if manager.get_user_by_name(form.username.data):
            return render_template(
                'register.html',
                form=form,
                message='Username is taken'
            )
        manager.create_user(form.nickname.data, form.username.data, str(form.birth_date.data), form.password.data)
        return redirect('/login')
    return render_template('register.html', form=form)


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        manager = DbManager()
        user = manager.get_user_by_name(form.username.data)
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