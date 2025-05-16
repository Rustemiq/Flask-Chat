import sqlalchemy
from data.models.db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


user_to_chat = sqlalchemy.Table(
    "user_to_chat",
    SqlAlchemyBase.metadata,
    sqlalchemy.Column("chats", sqlalchemy.Integer, sqlalchemy.ForeignKey("chats.id")),
    sqlalchemy.Column("users", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
)


class Chat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "chats"

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    members = orm.relationship("User", secondary="user_to_chat", back_populates="chats")
    messages = orm.relationship("Message", back_populates="chat")
