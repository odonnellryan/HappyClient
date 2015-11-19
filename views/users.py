from flask import Blueprint, render_template, request, flash, session, redirect, url_for, g
from views.forms import NewUserForm, LoginForm
from db import User, Company, Interaction, Client
from flask_login import login_user, login_required, current_user, logout_user
users = Blueprint('users', __name__, url_prefix='/users')

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
        company = g.company
        user = User().create(name=form.name, email=form.email.data, title=form.title.data,
                    secret_question=form.secret_question.data,
                    phone_number=form.phone_number.data, company=company.pk,
                    authentication_level=1)
        user.set_password(form.password.data)
        user.set_secret_answer(form.secret_answer.data)
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
        try:
            user = User().get(User.email==form.email.data)
        except User.DoesNotExist:
            flash('Invalid username and/or password.')
            return redirect(url_for('users.login'))
        if user.validate_login(plaintext_password=form.password.data):
            login_user(user)
            flash('Successfully logged in!')
            return redirect(url_for('company.home'))
        else:
            flash('Invalid username and/or password.')
    return render_template('user/login.html', form=form)


@users.route('/logout/')
def logout():
    logout_user()
    session.pop('company')
    return redirect(url_for('index'))


@users.route('/profile/')
@login_required
def profile():
    # where the user will edit their credentials
    return render_template('user/profile.html')
