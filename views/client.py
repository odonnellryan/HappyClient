from flask import Blueprint, render_template, request, flash, session, redirect, url_for, g
from flask_login import current_user
from db import Company, Client
from views.forms import NewClientForm
from utilities import flashed_errors
client = Blueprint('client', __name__, url_prefix='/client')

@client.route('/<int:client_pk>/')
@client.route('/')
def home(client_pk=None):
    form = NewClientForm(request.form)
    try:
        client = Client().get(Client.pk == client_pk, Client.company == current_user.company.pk)
        form.name.data = client.name
        form.location.data = client.location
        form.contact_information.data = client.contact_information
        form.interaction_reminder_notes.data = client.interaction_reminder_notes
        form.interaction_reminder_time.data = client.interaction_reminder_time
        form.notes.data = client.notes
    except Client.DoesNotExist:
        flash(flashed_errors.CLIENT_DOESNT_EXIST)
        return redirect(url_for('company.home'))

    return render_template('client/home.html', client=client, form=form)

@client.route('/new/', methods=['GET', 'POST'])
def new():
    form = NewClientForm(request.form)
    if request.method == 'POST' and form.add_client.data and form.validate():
        client = Client().create(name=form.name.data, contact_information=form.contact_information.data,
                                 location=form.location.data, notes=form.notes.data,
                                 interaction_reminder_time=form.interaction_reminder_time.data,
                                 interaction_reminder_notes=form.interaction_reminder_notes.data, company=g.company.pk,
                                 user=current_user.pk)
        return redirect(url_for('company.home', client_id=client.pk))
    return render_template('client/new.html', form=form)


@client.route('/edit/<int:client_pk>/')
@client.route('/edit/', methods=['GET', 'POST'])
def edit(client_pk=None):
    """
    edits the company information
    :return:
    """
    form = NewClientForm(request.form)
    if 'company' in session:
        company = Company(pk=session['company'])
    else:
        return redirect(url_for('company.new'))
    if request.method == 'POST' and form.validate():
        information = {'name': form.name.data,
                    'phone_number': form.phone_number.data,
                    'address': form.address.data}
        company.change_information(**information)
        #
        # store company PK, we'll have to get the company each time we
        # would like to view it
        # can probably store this in flask login as well, possibly
        #
        session['company'] = company.data.pk
        return redirect(url_for('company.home'))
    form.name.data = company.data.name
    form.address.data = company.data.address
    form.phone_number.data = company.data.phone_number
    return render_template('company/edit.html', form=form)