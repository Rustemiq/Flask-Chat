from wtforms import SubmitField, FieldList, FormField

from forms.chat_create import ChatCreationForm, UsernameForm


class ChatEditForm(ChatCreationForm):
    delete = SubmitField('Delete')
    usernames = FieldList(FormField(UsernameForm), min_entries=0)