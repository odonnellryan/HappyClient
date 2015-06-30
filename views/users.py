from flask import Blueprint, render_template

users = Blueprint('user', __name__)

@users.route('/')
def home():
    # user homepage
    return render_template('user/home.html')

@users.route('/register')
def register():
    # Do some stuff
    return render_template('user/register.html')

@users.route('/login')
def register():
    # Do some stuff
    return render_template('user/login.html')

@users.route('/about')
def about():
    # Do some stuff
    return render_template('user/profile.html')