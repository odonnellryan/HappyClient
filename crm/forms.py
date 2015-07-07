from utilities import helper_functions
from wtforms import StringField, TextAreaField, DateTimeField
from wtforms.validators import DataRequired


class NewClientForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_information = TextAreaField('Contact Information')
    location = StringField('Location')
    interaction_reminder_time = DateTimeField('Set contact reminder')
    interaction_reminder_notes = TextAreaField('Add notes regarding contact reminder')
    notes = TextAreaField('Notes')

class CompanyForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    phone_number = TextAreaField('Phone Number')
    address = StringField('Address')
