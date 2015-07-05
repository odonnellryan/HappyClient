from flask import Flask, render_template
from flask.ext.login import LoginManager
from user import user
from peewee import *
from flask_wtf.csrf import CsrfProtect
from views import users


app = Flask(__name__)
database = PostgresqlDatabase('my_app.db')
login_manager = LoginManager()
login_manager.init_app(app)

CsrfProtect(app)
app.secret_key = 'super secret key'
app.register_blueprint(users.users)
# this does not currently do much... will work on the web side after we have a basic app.


@login_manager.user_loader
def load_user(request):
    # this exists for flask-login
    return user.User(request.form['email'], request.form['password'])

#@app.before_request
#def _db_connect():
#    database.connect()
#
#@app.teardown_request
#def _db_close(exc):
#    if not database.is_closed():
#        database.close()

@app.route('/')
def index():
   return render_template('index.html')

app.debug = True

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('C:\\Users\\Ryan\\Documents\\happyclient.log', maxBytes=2048, backupCount=999)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':

    app.run()


