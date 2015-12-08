from flask import Blueprint, render_template, request, flash, session, redirect, url_for, g
from flask_login import current_user
from db import Company, Client
from views.forms import NewCompanyForm, ClientSearchForm
import exceptions

company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/<int:client_id>/')
@company.route('/')
def home(client_id=None):

    try:
        client = Client().get(Client.pk == client_id)
    except Client.DoesNotExist:
        client = None
    form = ClientSearchForm(request.form)
    if current_user.is_authenticated():
        session['company'] = current_user.company.pk
    if not 'company' in session:
        return redirect(url_for('company.new'))
    try:
        company = Company.get(Company.pk == session['company'])
    except Company.DoesNotExist:
        session.pop('company')
        flash("Sorry, it seems you were trying to access an invalid company.")
        return url_for('company.new')
    return render_template('company/home.html', company=company, form=form, client=client)


@company.route('/new/', methods=['GET', 'POST'])
def new():
    # also check if user logged in
    # since all users _must_ have an associated company
    form = NewCompanyForm(request.form)
    if 'company' in session:
        return redirect(url_for('company.home'))
    if request.method == 'POST' and form.validate():
        company = Company().create(name=form.name.data, phone_number=form.phone_number.data,
                               address=form.address.data)
        session['company'] = company.pk
        return redirect(url_for('company.home'))
    return render_template('company/new.html', form=form)


@company.route('/edit/', methods=['GET', 'POST'])
def edit():
    """
    edits the company information
    :return:
    """
    form = NewCompanyForm(request.form)
    if 'company' in session:
        company = Company.get(Company.pk == session['company'])
    else:
        return redirect(url_for('company.new'))
    if request.method == 'POST' and form.validate():
        information = {'name': form.name.data,
                       'phone_number': form.phone_number.data,
                       'address': form.address.data}
        query = Company().update(**information).where(Company.pk == company.pk)
        query.execute()
        session['company'] = company.pk
        return redirect(url_for('company.home'))
    form.name.data = company.name
    form.address.data = company.address
    form.phone_number.data = company.phone_number
    return render_template('company/edit.html', form=form)
