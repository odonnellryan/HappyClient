from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from user.forms import NewUserForm
from user.user import User

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/')
def home():
    # user homepage
    return render_template('user/home.html')


@users.route('/register/', methods=['GET', 'POST'])
def register():
    if 'company' not in session:
        return redirect(url_for('company.new'))
    form = NewUserForm(request.form)
    print(form.validate())
    print(form.errors)
    if request.method == 'POST' and form.validate():
        print('worked?')
        user = User()
        user.create(name=form.name, plaintext_password=form.password.data, email=form.email.data, title=form.title.data,
                    secret_question=form.secret_question.data, plaintext_secret_answer=form.secret_answer.data,
                    phone_number=form.phone_number.data, company=session['company'],
                    authentication_level=1)
        flash('Thanks for registering!')
    return render_template('user/register.html', form=form)


@users.route('/login/')
def login():
    return render_template('user/login.html')


@users.route('/profile/')
def profile():
    # where the user will edit their credentials
    return render_template('user/profile.html')
