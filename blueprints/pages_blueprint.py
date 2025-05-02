from flask import Blueprint, render_template, redirect
from flask_login import current_user

from data.db_manager import DbManager
from forms.message_writing import MessageForm

blueprint = Blueprint(
    'pages_function',
    __name__,
    template_folder='templates'
)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        chats = current_user.chats
    else:
        chats = []
    return render_template('home.html', chats=chats)


@blueprint.route('/chat/<int:chat_id>', methods=['GET', 'POST'])
def chat(chat_id):
    manager = DbManager()
    chat = manager.get_chat(chat_id)
    if not current_user.is_authenticated or not current_user in chat.members:
        return redirect('/')
    form = MessageForm()
    if form.validate_on_submit():
        manager.create_message(chat_id, current_user.id, form.text.data)
    return render_template('chat.html', chat=chat, form=form)