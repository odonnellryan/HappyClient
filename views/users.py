from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from user.forms import LoginForm
from views.forms import NewUserForm, LoginForm
from db import User
from tests.company import Company
from flask_login import login_user, login_required, current_user, logout_user
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
                    phone_number=form.phone_number.data, company=company.data.pk,
                    authentication_level=1)
        flash('Thanks for registering!')
        return form.redirect()
    return render_template('user/register.html', form=form)


@users.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    print(current_user.is_authenticated)
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    if request.method == 'POST' and form.validate():
        user = User()
        try:
            user.set(email=form.email.data)
        except Exception as e:
            # TODO: will eventually log this
            print(e)
            flash('Invalid username and/or password.')
            return redirect(url_for('users.login'))
        if user.validate_login(plaintext_password=form.password.data):
            login_user(user)
            flash('Successfully logged in!')
            return form.redirect()
        else:
            flash('Invalid username and/or password.')
    return render_template('user/login.html', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))


@users.route('/profile/')
@login_required
def profile():
    # where the user will edit their credentials
    return render_template('user/profile.html')
