from utilities import helper_functions
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ClientForm(helper_functions.RedirectForm):
    name = StringField('Name', validators=[DataRequired()])
    contact_information = TextAreaField('Contact Information')
    location = StringField('Location')
    notes = TextAreaField('Notes')
