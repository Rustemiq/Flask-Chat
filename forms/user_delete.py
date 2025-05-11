from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class UserDeleteForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    agreement = BooleanField('Deletion is irreversible. Are you sure?')
    submit = SubmitField('Delete')