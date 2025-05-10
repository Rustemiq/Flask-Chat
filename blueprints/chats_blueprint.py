from flask import Blueprint, render_template, redirect
from flask_login import current_user
from flask_uploads import UploadSet
from transliterate import translit

from data.db_manager import DbManager
from forms.chat_creation import ChatCreationForm
from forms.message_writing import MessageForm

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


@blueprint.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    if not current_user.is_authenticated or not current_user in chat.members:
        return redirect('/')
    form = MessageForm()
    if form.validate_on_submit():
        message = manager.create_message(chat_id, current_user.id, form.text.data)
        messages = UploadSet('messages')
        for file in form.files.data:
            if file.filename != '':
                user_filename = file.filename
                file.filename = translit(file.filename, language_code='ru', reversed=True)
                filename = messages.save(file)
                manager = DbManager()
                manager.create_file(filename, user_filename, message.id)
    return render_template('chat.html', chat=chat, form=form)