from utilities import helper_functions
from wtforms import StringField, TextAreaField, PasswordField, SubmitField
from wtforms_components import DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo


class NewClientForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_information = TextAreaField('Contact Information')
    location = StringField('Location')
    interaction_reminder_time = DateTimeField('Set contact reminder')
    interaction_reminder_notes = TextAreaField('Add notes regarding contact reminder')
    notes = TextAreaField('Notes')
    add_client = SubmitField('Add Client')


class NewCompanyForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number')
    address = TextAreaField('Address')


class ClientSearchForm(helper_functions.Form):
    client = StringField('Name')


class NewUserForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    #authentication_level = SelectField(
    #    "User Privilege Level",
    #    choices=[(1, "Admin"), (2, "Super User"), (3, "User")],
    #    default=3)
    password = PasswordField(
        'Password',
        validators=[
            Length(min=8),
            DataRequired(message='Must supply a password.'),
            EqualTo('confirm', message='Passwords must match')]
        )
    confirm = PasswordField('Repeat password')
    email = StringField('Email', validators = [DataRequired()])
    title = StringField('Title')
    secret_question = StringField('Secret Question', validators=[DataRequired(message='Must supply secret question.')])
    secret_answer = PasswordField('Secret Answer',
                                  validators=[DataRequired(message='Must supply answer to secret question.')])
    phone_number = StringField('Phone Number')


class LoginForm(helper_functions.RedirectForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )