from flask import Blueprint, render_template, redirect
from flask_login import current_user
from requests import post, get

from forms.chat_creation import ChatCreationForm
from data.models import db_session
from data.users import User

blueprint = Blueprint(
    'chats_function',
    __name__,
    template_folder='templates'
)


@blueprint.route('/create_chat', methods=['GET', 'POST'])
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
            members = form.usernames.data
            members.append({'username': current_user.username})
            post('http://127.0.0.1:8080/api/chats', json={
                'name': form.name.data,
                'members': members
                })
            return redirect('/')
    return render_template(
        'chat_creation.html',
        form=form, not_found_users = []
    )
