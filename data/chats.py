import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


user_to_chat = sqlalchemy.Table(
    'user_to_chat',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('chats', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('chats.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class Chat(SqlAlchemyBase):
    __tablename__ = 'chats'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    members = orm.relationship("User",
                          secondary="user_to_chat",
                          backref="chat")