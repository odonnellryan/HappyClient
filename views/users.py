from flask import Blueprint, render_template

profile = Blueprint('user', __name__)

@profile.route('/')
def home():
    # user homepage
    return render_template('user/home.html')

@profile.route('/register')
def register():
    # Do some stuff
    return render_template('user/register.html')

@profile.route('/login')
def register():
    # Do some stuff
    return render_template('user/login.html')

@profile.route('/about')
def about():
    # Do some stuff
    return render_template('user/profile.html')