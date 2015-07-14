from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from crm.forms import CompanyForm
from crm.company import Company
company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def home():
    if not 'company' in session:
        return redirect(url_for('company.new'))
    # also check if user logged in
    return render_template('company/home.html')

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
        session['company'] = company
        return redirect(url_for('company.home'))
    return render_template('company/new.html', form=form)