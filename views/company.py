from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from crm.forms import CompanyForm
from crm.company import Company
import exceptions
company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def home():
    if not 'company' in session:
        return redirect(url_for('company.new'))
    try:
        company = Company(pk=session['company'])
    except exceptions.CompanyInvalid:
        session.pop('company')
        flash("Sorry, it seems you were trying to access an invalid company.")
        return url_for('company.new')
    return render_template('company/home.html', company=company.data)

@company.route('/new/', methods=['GET', 'POST'])
def new():
    # also check if user logged in
    # since all users _must_ have an associated company
    form = CompanyForm(request.form)
    if 'company' in session:
        return redirect(url_for('company.home'))
    if request.method == 'POST' and form.validate():
        company = Company()
        company.create_company(form.name.data, form.phone_number.data,
                               form.address.data)
        #
        # store company PK, we'll have to get the company each time we
        # would like to view it
        # can probably store this in flask login as well, possibly
        #
        session['company'] = company.data.pk
        return redirect(url_for('company.home'))
    return render_template('company/new.html', form=form)

@company.route('/edit/', methods=['GET', 'POST'])
def edit():
    """
    edits the company information
    :return:
    """
    form = CompanyForm(request.form)
    if 'company' in session:
        company = Company(pk=session['company'])
    else:
        return redirect(url_for('company.new'))
    if request.method == 'POST' and form.validate():
        company = Company()
        company.create_company(form.name.data, form.phone_number.data,
                               form.address.data)
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