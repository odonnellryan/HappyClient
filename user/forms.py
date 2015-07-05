from wtforms import Form
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    authentication_level = SelectField(
        "User Privilege Level",
        choices=[(1, "Admin"), (2, "Super User"), (3, "User")],
        default=3)
    password = PasswordField(
        'Password',
        validators=[
            Length(min=8),
            DataRequired(),
            EqualTo('confirm', message='Passwords must match')]
        )
    confirm = PasswordField('Repeat password')
    email = StringField('Email', validators = [DataRequired()])
    title = StringField('Title')
    secret_question = StringField('Secret Question', validators = [DataRequired(message='Must supply secret question.')])
    secret_answer = PasswordField('Secret Answer',
                                  validators = [DataRequired(message='Must supply answer to secret question.')])
    phone_number = StringField('Phone Number')


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )