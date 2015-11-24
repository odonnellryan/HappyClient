from flask import Blueprint, g, jsonify, session
from db import Client, Interaction
from collections import OrderedDict
from playhouse.shortcuts import model_to_dict

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/search/<path:search_term>/', methods=['GET'])
def search_clients(search_term=None):
    """
    searches clients
    :param search_term:
    :return:
    """

    if 'recent_clients' not in session:
        session['recent_clients'] = OrderedDict(last=True)

    if search_term is None:
        return jsonify({'errors': "No search term"})

    clients = (
        Client.select().where((Client.company == g.company) & (
            (Client.name ** search_term) |
            (Client.contact_information ** search_term) |
            (Client.location ** search_term) |
            (Client.notes ** search_term))
        )
    )

    results = [model_to_dict(client) for client in clients]

    for item in results:
        session['recent_clients'][item['name']] = item

    while len(session['recent_clients']) > 10:
        session['recent_clients'].pop()

    print(session['recent_clients'])

    values = {
        'clients': results
    }

    return jsonify(values)