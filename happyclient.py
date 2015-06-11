from flask import Flask
from flask.ext.login import LoginManager
from users import user
app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return user.User(user_id)


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
