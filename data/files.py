import sqlalchemy
from data.models.db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class File(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'files'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user_filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    message_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("messages.id"))
    message = orm.relationship('Message')
