from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired


class ClientForm(Form):
    name = StringField('Name', validators=[DataRequired()])
    contact_information = TextAreaField('Contact Information')
    location = StringField('Location')
    notes = TextAreaField('Notes')
