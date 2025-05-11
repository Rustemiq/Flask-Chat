from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField
from wtforms.validators import DataRequired, InputRequired


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired()])
    password_again = PasswordField('Repeat', validators=[DataRequired()])
    submit = SubmitField('Submit')