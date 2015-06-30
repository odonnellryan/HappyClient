from flask_wtf import Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, AnyOf

class UserForm(Form):
    name = StringField('name', validators=[DataRequired()])
    authentication_level = IntegerField(
        'authentication_level',
        validators = [
            DataRequired(),
            AnyOf((1, 2, 3))
        ])
    password = PasswordField(
        'password',
        validators = [
            Length(min=8),
            DataRequired(),
            EqualTo('confirm', message='Passwords must match')
        ])
    confirm = PasswordField('Repeat password')
    email = StringField('email', validators = [DataRequired()])
    title = StringField('title')
    secret_question = StringField('secret_question')
    secret_answer = PasswordField('secret_answer')