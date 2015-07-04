from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from user.forms import RegistrationForm
from user.user import User
users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/')
def home():
    # user homepage
    return render_template('user/home.html')


@users.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.create_user(name=form.name, plaintext_password=form.password, email=form.email, title=form.title,
                         secret_question=form.secret_question, plaintext_secret_answer=form.secret_answer,
                         phone_number=form.phone_number,company=session['company'],
                         authentication_level=form.authentication_level)

        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('user/register.html')


@users.route('/login/')
def login():
    return render_template('user/login.html')


@users.route('/profile/')
def profile():
    # where the user will edit their credentials
    return render_template('user/profile.html')
