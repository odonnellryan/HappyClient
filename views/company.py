from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from user.forms import NewUserForm
from user.user import User
company = Blueprint('company', __name__, url_prefix='/company')

@company.route('/')
def home():
    if not 'company' in session:
        return redirect(url_for('company.new'))
    return render_template('company/home.html')

@company.route('/new/', methods=['GET', 'POST'])
def new():
    return render_template('company/new.html')