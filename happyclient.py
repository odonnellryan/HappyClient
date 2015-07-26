from flask import Flask, render_template, url_for
from flask.ext.login import LoginManager
import user.user as user
from flask_wtf.csrf import CsrfProtect
from views import users, company
import exceptions
import config
import db

def create_tables():
    pass
    #db.database.connect()
    # # try to create the tables (first run) if exception is thrown,
    # # pass. Can probably use some other way to check this but for now
    # # it is fine
    #try:
    #    db.database.create_tables([
    #                        db.Interaction])
    #except OperationalError as e:
    #    print(e)
    #  #  pass

app = Flask(__name__)

app.debug = config.debug

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

CsrfProtect(app)

app.secret_key = 'super secret key'
app.register_blueprint(users.users)
app.register_blueprint(company.company)

@login_manager.user_loader
def load_user(user_pk):
    _user = user.User()
    try:
        _user.set(pk=user_pk)
    except exceptions.UserInvalid:
        return None
    else:
        return _user

@app.before_request
def _db_connect():
    db.database.connect()

@app.teardown_request
def _db_close(exc):
    if not db.database.is_closed():
        db.database.close()

@app.route('/')
def index():
   return render_template('index.html')

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('C:\\Users\\Ryan\\Documents\\happyclient.log', maxBytes=2048, backupCount=999)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    create_tables()
    app.run()


