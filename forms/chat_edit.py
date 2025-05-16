from wtforms import FieldList, FormField

from forms.chat_create import ChatCreationForm, UsernameForm


class ChatEditForm(ChatCreationForm):
    usernames = FieldList(FormField(UsernameForm), min_entries=0)