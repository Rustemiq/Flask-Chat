from flask import Blueprint, render_template, redirect, send_file
from flask_login import current_user, login_required
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


@login_required
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
            for form_username in form.usernames:
                username = form_username.data['username']
                if not manager.get_user_by_name(username) or username == current_user.username:
                    not_found_users.append(form_username)
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
@login_required
def chat(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    if not current_user in chat.members:
        return redirect('/')
    form = MessageForm()
    upload_messages = UploadSet('messages')
    if form.validate_on_submit():
        message = manager.create_message(chat_id, current_user.id, form.text.data)
        for file in form.files.data:
            if file.filename != '':
                user_filename = file.filename
                file.filename = translit(file.filename, language_code='ru', reversed=True)
                filename = upload_messages.save(file)
                manager = DbManager()
                manager.create_file(filename, user_filename, message.id)
    return render_template('chat.html', chat=chat, form=form, upload_messages=upload_messages)


@blueprint.route('/chat_members/<int:chat_id>')
@login_required
def members(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    if current_user not in chat.members:
        return redirect('/')
    return render_template('members.html', chat=chat)


@blueprint.route('/kick/<int:user_id>/<int:chat_id>')
@login_required
def kick(user_id, chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    user = manager.get_user(user_id)
    if current_user not in chat.members:
        return redirect('/')
    chat.members.remove(user)
    if chat.members == []:
        manager.delete_chat(chat.id)
    if user == current_user:
        return redirect('/')
    return render_template('members.html', chat=chat)


@blueprint.route('/download/<file_id>')
@login_required
def download(file_id):
    manager = DbManager()
    file = manager.get_file(file_id)
    if not current_user in file.message.chat.members:
        return redirect('/')
    upload_messages = UploadSet('messages')
    path = upload_messages.url(file.filename)
    return send_file(path, download_name=file.user_filename, as_attachment=True)

