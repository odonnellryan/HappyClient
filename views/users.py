from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from user.forms import NewUserForm, LoginForm
from user.user import User
from crm.company import Company
from flask_login import login_user
users = Blueprint('users', __name__, url_prefix='/users')
import exceptions

@users.route('/')
def home():
    # user homepage
    return render_template('user/home.html')


@users.route('/register/', methods=['GET', 'POST'])
def register():
    # check if user already logged in
    if 'company' not in session:
        return redirect(url_for('company.new'))
    form = NewUserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        company = Company(pk=session['company'])
        user.create(name=form.name, plaintext_password=form.password.data, email=form.email.data, title=form.title.data,
                    secret_question=form.secret_question.data, plaintext_secret_answer=form.secret_answer.data,
                    phone_number=form.phone_number.data, company=company,
                    authentication_level=1)
        flash('Thanks for registering!')
    return render_template('user/register.html', form=form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        try:
            user.set(email=form.email.data)
        except Exception as e:
            # TODO: will eventually log this
            print(e)
            redirect(url_for(register))
        if user.validate_login(plaintext_password=form.password.data):
            login_user(user)
            redirect(url_for('home'))
        else:
            flash("User credentials invalid.")
    return render_template('user/login.html')


@users.route('/profile/')
def profile():
    # where the user will edit their credentials
    return render_template('user/profile.html')
