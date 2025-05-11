from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, DateField
from wtforms.validators import DataRequired, InputRequired


class UserEditForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    birth_date = DateField('Birth date', validators=[InputRequired()])
    submit = SubmitField('Submit')