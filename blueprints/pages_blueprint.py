from flask import Blueprint, render_template, redirect
from flask_login import current_user
from requests import get

blueprint = Blueprint(
    'pages_function',
    __name__,
    template_folder='templates'
)


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    if current_user.is_authenticated:
        chats_id = get(f'http://127.0.0.1:8080/api/users/{current_user.id}').json()['users']['chats']
    else:
        chats_id = []
    chats = []
    for chat_id in chats_id:
        chat = get(f'http://127.0.0.1:8080/api/chats/{chat_id}').json()['chats']
        chats.append(chat)
    return render_template('home.html', chats=chats)