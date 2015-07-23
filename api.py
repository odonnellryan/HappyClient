from flask import Flask, render_template, Blueprint
import db

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/search/<model>/<search_term>/', methods=['GET'])
def search(model, search_term):
    allowed_models = {'client': db.Client, 'interactions': db.Interaction}
    if model not in allowed_models:
        return {}


# future home of some functions for the happyclient API
# will probably put the client/all search function in here.