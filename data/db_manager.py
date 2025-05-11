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

    def get_file(self, file_id):
        return self.db_sess.query(File).filter(File.id == file_id).first()

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

    def edit_user(self, user_id, **params):
        user = self.get_user(user_id)
        user.nickname = params.get('nickname', user.nickname)
        user.username = params.get('username', user.username)
        user.birth_date = params.get('birth_date', user.birth_date)
        if 'password' in params.keys():
            user.set_password(params['password'])

    def edit_chat(self, chat_id, **params):
        chat = self.get_chat(chat_id)
        chat.name = params.get('name', chat.name)
        for username in params.get('new_members', []):
            chat.members.append(self.get_user_by_name(username))

    def edit_message(self, message_id, text):
        message = self.get_message(message_id)
        message.text = text

    def delete_user(self, user_id):
        user = self.get_user(user_id)
        for chat in user.chats:
            for message in chat.messages:
                if message.author_id == user_id:
                    self.edit_message(message.id, 'User has been deleted')
                    for file in message.files:
                        self.delete_file(file.id)
                    message.author_id = None
        self.db_sess.delete(user)
        self.db_sess.commit()

    def delete_chat(self, chat_id):
        chat = self.get_chat(chat_id)
        chat.members = []
        for message in chat.messages:
            self.delete_message(message.id)
        self.db_sess.delete(chat)
        self.db_sess.commit()

    def delete_message(self, message_id):
        message = self.get_message(message_id)
        for file in message.files:
            self.delete_file(file.id)
        self.db_sess.delete(message)
        self.db_sess.commit()

    def delete_file(self, file_id):
        file = self.get_file(file_id)
        self.db_sess.delete(file)
        self.db_sess.commit()
