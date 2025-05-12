from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField


class ChatDeleteForm(FlaskForm):
    agreement = BooleanField('Deletion is irreversible. Are you sure?')
    submit = SubmitField('Delete')