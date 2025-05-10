from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    files = MultipleFileField('Files')
    submit = SubmitField('Send')