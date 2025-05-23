from flask import Blueprint, render_template, redirect, send_file
from flask_login import current_user, login_required
from flask_uploads import UploadSet
from transliterate import translit

from data.db_manager import DbManager
from forms.chat_create import ChatCreationForm
from forms.chat_delete import ChatDeleteForm
from forms.chat_edit import ChatEditForm
from forms.message_edit import MessageEditForm
from forms.message_write import MessageForm
from tools.abort_if_no_access import abort_if_not_member, abort_if_not_msg_author
from tools.abort_if_not_found import abort_if_not_found

blueprint = Blueprint("chats_function", __name__, template_folder="templates")


@login_required
@blueprint.route("/create_chat", methods=["GET", "POST"])
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
                username = form_username.data["username"]
                if (
                    not manager.get_user_by_name(username)
                    or username == current_user.username
                ):
                    not_found_users.append(form_username)
            if not_found_users:
                return render_template(
                    "chat_creation.html", form=form, not_found_users=not_found_users
                )
            members_names = [member["username"] for member in form.usernames.data]
            members_names.append(current_user.username)
            manager.create_chat(form.name.data, members_names)
            return redirect("/")
    return render_template("chat_creation.html", form=form, not_found_users=[])


@blueprint.route("/chat/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    abort_if_not_found(chat)
    abort_if_not_member(current_user, chat)
    form = MessageForm()
    upload_messages = UploadSet("messages")
    if form.validate_on_submit():
        message = manager.create_message(chat_id, current_user.id, form.text.data)
        for file in form.files.data:
            if file.filename != "":
                user_filename = file.filename
                file.filename = translit(
                    file.filename, language_code="ru", reversed=True
                )
                filename = upload_messages.save(file)
                manager = DbManager()
                manager.create_file(filename, user_filename, message.id)
    return render_template(
        "chat.html", chat=chat, form=form, upload_messages=upload_messages
    )


@blueprint.route("/chat_edit/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_edit(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    abort_if_not_found(chat)
    abort_if_not_member(current_user, chat)
    form = ChatEditForm(name=chat.name)
    if form.validate_on_submit():
        if form.add_user.data:
            form.usernames.append_entry()
        elif form.delete_user.data:
            if form.usernames.__len__() > 0:
                form.usernames.pop_entry()
        elif form.confirm.data:
            not_found_users = []
            for form_username in form.usernames:
                username = form_username.data["username"]
                user = manager.get_user_by_name(username)
                if not user or user in chat.members:
                    not_found_users.append(form_username)
            if not_found_users:
                return render_template(
                    "chat_edit.html",
                    chat=chat,
                    form=form,
                    not_found_users=not_found_users,
                )
            members_names = [member["username"] for member in form.usernames.data]
            manager.edit_chat(chat.id, name=form.name.data, new_members=members_names)
            return render_template("chat_edit.html", chat=chat, form=form)
    return render_template("chat_edit.html", chat=chat, form=form)


@blueprint.route("/chat_delete/<int:chat_id>", methods=["GET", "POST"])
@login_required
def chat_delete(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    abort_if_not_found(chat)
    abort_if_not_member(current_user, chat)
    form = ChatDeleteForm()
    if form.validate_on_submit() and form.agreement.data:
        manager.delete_chat(chat.id)
        return redirect("/")
    return render_template("chat_delete.html", chat=chat, form=form)


@blueprint.route("/select_message/<int:chat_id>", methods=["GET", "POST"])
@login_required
def select_message(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    abort_if_not_found(chat)
    abort_if_not_member(current_user, chat)
    return render_template("select_message.html", chat=chat)


@blueprint.route("/message_edit/<int:message_id>", methods=["GET", "POST"])
@login_required
def message_edit(message_id):
    manager = DbManager()
    message = manager.get_message(message_id)
    abort_if_not_found(message)
    abort_if_not_msg_author(current_user, message)
    abort_if_not_member(current_user, message.chat)
    form = MessageEditForm(text=message.text)
    if form.validate_on_submit():
        manager.edit_message(message.id, form.text.data)
        return redirect(f"/chat/{message.chat.id}")
    return render_template("message_edit.html", message=message, form=form)


@blueprint.route("/message_delete/<int:message_id>", methods=["GET", "POST"])
@login_required
def message_delete(message_id):
    manager = DbManager()
    message = manager.get_message(message_id)
    abort_if_not_found(message)
    abort_if_not_msg_author(current_user, message)
    abort_if_not_member(current_user, message.chat)
    chat_id = message.chat.id
    manager.delete_message(message.id)
    return redirect(f"/chat/{chat_id}")


@blueprint.route("/kick/<int:user_id>/<int:chat_id>")
@login_required
def kick(user_id, chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    user = manager.get_user(user_id)
    abort_if_not_found(chat)
    abort_if_not_found(user)
    abort_if_not_member(user, chat)
    abort_if_not_member(current_user, chat)
    chat.members.remove(user)
    if chat.members == []:
        manager.delete_chat(chat.id)
    if user == current_user:
        return redirect("/")
    return redirect(f"/chat_edit/{chat.id}")


@blueprint.route("/download/<file_id>")
@login_required
def download(file_id):
    manager = DbManager()
    file = manager.get_file(file_id)
    abort_if_not_found(file)
    abort_if_not_member(current_user, file.message.chat)
    upload_messages = UploadSet("messages")
    path = upload_messages.url(file.filename)
    return send_file(path, download_name=file.user_filename, as_attachment=True)

    abort_if_not_found(file)
    abort_if_not_member(current_user, file.message.chat)
    upload_messages = UploadSet('messages')
    path = upload_messages.url(file.filename)
    return send_file(path, download_name=file.user_filename, as_attachment=True)

