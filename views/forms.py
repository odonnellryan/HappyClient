from utilities import helper_functions
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, AnyOf
import datetime
import operator


class DateAfterValidator:
    def __init__(self, op, obj, message=None):
        self.obj = obj
        self.operator = op
        if not message:
            message = u'Field does not meet date requirements.'
        self.message = message

    def __call__(self, form, field):
        l = field.data
        date = datetime.datetime.strptime(l, "%m/%d/%Y %I:%M %p")
        if not self.operator(date, self.obj):
            raise ValidationError(self.message)


class NewClientForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_information = TextAreaField('Contact Information')
    location = StringField('Location')
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

class InteractionForm(helper_functions.Form):
    add_interaction = SubmitField('Add Interaction')
    interaction_reminder_time = StringField('Interaction reminder',
                       validators=[DataRequired(),
                                   DateAfterValidator(operator.ge, datetime.datetime.now(),
                       message="Date must be sometime in the future.")])
    rating = RadioField('Please leave a rating', choices=[("1", "1"), ("2", "2"), ("3", "3")],
                        validators=[AnyOf(['1', '2', '3'])])
    interaction_reminder_notes = TextAreaField('Interaction notes')
    sale = StringField('Sale amount', default=None)