from flask import Flask, render_template, url_for
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from views import users, company
import config
from db import database, User, Interaction
from peewee import OperationalError

from flask.ext.login import AnonymousUserMixin


class Anonymous(AnonymousUserMixin):
    def __init__(self):
        self.is_validated = 'Guest'


def create_tables():
    database.connect()
    # try to create the tables (first run) if exception is thrown,
    # pass. Can probably use some other way to check this but for now
    # it is fine
    try:
        database.create_tables([Interaction, User])
    except OperationalError as e:
        print(e)
        pass


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
    user = User().get(pk=user_pk)
    try:
        user
    except User.DoesNotExist:
        return None
    else:
        return user


@app.before_request
def _db_connect():
    database.connect()


@app.teardown_request
def _db_close(exec):
    if not database.is_closed():
        database.close()


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
    app.run(port=5050)
