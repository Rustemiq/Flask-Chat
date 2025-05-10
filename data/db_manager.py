from data.chats import Chat
from data.files import File
from data.messages import Message
from data.models import db_session
from data.users import User
from tools.singleton import singleton


@singleton
class DbManager():
    def __init__(self):
        self.db_sess = db_session.create_session()

    def get_user(self, user_id):
        return self.db_sess.query(User).filter(User.id == user_id).first()

    def get_user_by_name(self, username):
        return self.db_sess.query(User).filter(User.username == username).first()

    def get_chat(self, chat_id):
        return self.db_sess.query(Chat).filter(Chat.id == chat_id).first()

    def get_message(self, message_id):
        return self.db_sess.query(Message).filter(Message.id == message_id).first()

    def create_user(self, nickname, username, birth_date, password):
        user = User(
            nickname=nickname,
            username=username,
            birth_date=birth_date
        )
        user.set_password(password)
        self.db_sess.add(user)
        self.db_sess.commit()
        return user

    def create_chat(self, name, members_names):
        chat = Chat(name=name)
        for username in members_names:
            chat.members.append(self.get_user_by_name(username))
        self.db_sess.add(chat)
        self.db_sess.commit()
        return chat

    def create_message(self, chat_id, author_id, text):
        message = Message(
            chat_id=chat_id,
            author_id=author_id,
            text=text
        )
        self.db_sess.add(message)
        self.db_sess.commit()
        return message

    def create_file(self, filename, user_filename, message_id):
        file = File(
            filename=filename,
            user_filename=user_filename,
            message_id=message_id
        )
        self.db_sess.add(file)
        self.db_sess.commit()
        return file

