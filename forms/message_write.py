from flask_uploads import UploadSet
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileSize
from wtforms import SubmitField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired


messages = UploadSet("messages")


class MessageForm(FlaskForm):
    text = TextAreaField(validators=[DataRequired()])
    files = MultipleFileField(
        "Files", validators=[FileAllowed(messages, "Unsupported file extension")]
    )
    submit = SubmitField("Send")
