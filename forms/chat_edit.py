from wtforms import SubmitField, FieldList, FormField, BooleanField

from forms.chat_create import ChatCreationForm, UsernameForm


class ChatEditForm(ChatCreationForm):
    usernames = FieldList(FormField(UsernameForm), min_entries=0)