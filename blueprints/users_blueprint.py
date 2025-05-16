import datetime

from flask import Blueprint, redirect, render_template
from flask_login import login_user, login_required, logout_user, current_user

from data.db_manager import DbManager
from forms.user_edit import UserEditForm
from forms.user_login import LoginForm
from forms.user_register import RegisterForm
from forms.change_password import ChangePasswordForm
from forms.user_delete import UserDeleteForm
from tools.abort_if_no_access import abort_if_authenticated, abort_if_not_concrete_user
from tools.abort_if_not_found import abort_if_not_found

blueprint = Blueprint("users_function", __name__, template_folder="templates")


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    abort_if_authenticated(current_user)
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template(
                "register.html", form=form, message="Passwords do not match"
            )
        manager = DbManager()
        if manager.get_user_by_name(form.username.data):
            return render_template(
                "register.html", form=form, message="Username is taken"
            )
        manager.create_user(
            form.nickname.data,
            form.username.data,
            str(form.birth_date.data),
            form.password.data,
        )
        return redirect("/login")
    return render_template("register.html", form=form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    abort_if_authenticated(current_user)
    form = LoginForm()
    if form.validate_on_submit():
        manager = DbManager()
        user = manager.get_user_by_name(form.username.data)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template(
            "login.html", message="Wrong username or password", form=form
        )

    return render_template("login.html", form=form)


@blueprint.route("/profile/<int:user_id>", methods=["GET"])
def profile(user_id):
    manager = DbManager()
    user = manager.get_user(user_id)
    abort_if_not_found(user)
    return render_template("profile.html", user=user)


@blueprint.route("/profile_edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile_edit(user_id):
    manager = DbManager()
    user = manager.get_user(user_id)
    abort_if_not_found(user)
    abort_if_not_concrete_user(current_user, user)
    y, m, d = map(int, user.birth_date.split("-"))
    birth_date = datetime.date(y, m, d)
    form = UserEditForm(
        nickname=user.nickname, username=user.username, birth_date=birth_date
    )
    if form.validate_on_submit():
        manager.edit_user(
            user.id,
            nickname=form.nickname.data,
            username=form.username.data,
            birth_date=str(form.birth_date.data),
        )
        return redirect(f"/profile/{user_id}")
    return render_template("profile_edit.html", user=user, form=form)


@blueprint.route("/profile_delete/<int:user_id>", methods=["GET", "POST"])
@login_required
def profile_delete(user_id):
    form = UserDeleteForm()
    manager = DbManager()
    user = manager.get_user(user_id)
    abort_if_not_found(user)
    abort_if_not_concrete_user(current_user, user)
    if form.validate_on_submit() and form.agreement.data:
        if not user.check_password(form.password.data):
            return render_template(
                "profile_delete.html", form=form, message="Wrong password"
            )
        manager.delete_user(user_id)
        return redirect("/")
    return render_template("profile_delete.html", form=form)


@blueprint.route("/change_password/<int:user_id>", methods=["GET", "POST"])
@login_required
def change_password(user_id):
    form = ChangePasswordForm()
    manager = DbManager()
    user = manager.get_user(user_id)
    abort_if_not_found(user)
    abort_if_not_concrete_user(current_user, user)
    if form.validate_on_submit():
        if not user.check_password(form.old_password.data):
            return render_template(
                "change_password.html",
                user=user,
                form=form,
                message="Wrong old password",
            )
        if form.password.data != form.password_again.data:
            return render_template(
                "change_password.html",
                user=user,
                form=form,
                message="Passwords do not match",
            )
        manager.edit_user(user.id, password=form.password.data)
        return redirect(f"/profile_edit/{user.id}")
    return render_template("change_password.html", user=user, form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")