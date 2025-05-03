from flask import Blueprint, render_template
from flask_login import current_user

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