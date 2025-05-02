from flask import Blueprint, render_template, redirect
from flask_login import current_user

from data.db_manager import DbManager
from forms.chat_creation import ChatCreationForm


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
            manager = DbManager()
            not_found_users = []
            for username in form.usernames:
                if not manager.get_user_by_name((username.data['username'])):
                    not_found_users.append(username)
            if not_found_users:
                return render_template(
                    'chat_creation.html',
                    form=form,
                    not_found_users=not_found_users
                )
            members_names = [member['username'] for member in form.usernames.data]
            members_names.append(current_user.username)
            manager.create_chat(form.name.data, members_names)
            return redirect('/')
    return render_template(
        'chat_creation.html',
        form=form, not_found_users = []
    )
