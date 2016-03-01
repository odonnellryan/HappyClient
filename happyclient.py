from flask import Flask, render_template, url_for, session, g, redirect
from flask.ext.login import LoginManager, current_user
from flask_wtf.csrf import CsrfProtect
from views import users, company, client, api, interaction
import config
from db import database, User, Interaction, Company, Client
from peewee import OperationalError


def create_tables():
    database.connect()
    tables = [Interaction, User, Company, Client]
    for table in tables:
        try:
            database.create_table(table)
        except OperationalError:
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
app.register_blueprint(client.client)
app.register_blueprint(api.api)
app.register_blueprint(interaction.interaction)


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
def before_request():
    create_tables()
    if 'company' in session:
        try:
            g.company = Company().get(Company.pk == session['company'])
        except Company.DoesNotExist:
            g.company = None
            session.pop('company')
    if 'recent_clients' in session:
        g.recent_clients = session['recent_clients']
    if current_user.is_authenticated():
        g.company = current_user.company
        session['company'] = g.company.pk
    database.connect()


@app.teardown_request
def _db_close(e):
    if not database.is_closed():
        database.close()


@app.route('/')
def index():
    if current_user.is_authenticated():
        return redirect(url_for('company.home'))
    return render_template('index.html')


if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler

    file_handler = RotatingFileHandler('C:\\Users\\Ryan\\Documents\\happyclient.log', maxBytes=2048, backupCount=999)
    file_handler.setLevel(logging.WARNING)
    app.logger.addHandler(file_handler)

if __name__ == '__main__':
    app.run(port=5050)
