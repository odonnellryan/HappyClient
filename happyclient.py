from flask import Flask
from flask.ext.login import LoginManager
from users import user
from peewee import *
app = Flask(__name__)
database = PostgresqlDatabase('my_app.db')
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user.User(user_id)

@app.before_request
def _db_connect():
    database.connect()

@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()

@app.route('/')
def hello_world():
    return 'Hello World!'

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('happyclient.log', maxBytes=2048, backupCount=999)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run()

from flask import Flask



