from flask import Blueprint, render_template

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/')
def home():
    # user homepage
    return render_template('user/home.html')


@users.route('/register/')
def register():
    return render_template('user/register.html')


@users.route('/login/')
def login():
    return render_template('user/login.html')


@users.route('/profile/')
def profile():
    # where the user will edit their credentials
    return render_template('user/profile.html')
