from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, Form, FieldList, FormField
from wtforms.validators import DataRequired, Optional


class UsernameForm(Form):
    username = StringField("Username", validators=[Optional()])


class ChatCreationForm(FlaskForm):
    name = StringField("Chat name", validators=[DataRequired()])
    usernames = FieldList(FormField(UsernameForm), min_entries=1)
    add_user = SubmitField("Add user")
    delete_user = SubmitField("Delete user")
    confirm = SubmitField("Submit")
