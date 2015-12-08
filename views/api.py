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

    cached_results_length = 10

    if 'recent_clients' not in session:
        session['recent_clients'] = OrderedDict()

    if search_term is None:
        return jsonify({'errors': "No search term"})

    clients = (
        Client.select().where((Client.company == g.company) & (
            (Client.name.contains(search_term)) |
            (Client.contact_information.contains(search_term)) |
            (Client.location.contains(search_term)) |
            (Client.notes.contains(search_term)))
        )
    )

    results = [model_to_dict(client) for client in clients]

    for item in results[:cached_results_length]:
        session['recent_clients'][item['pk']] = item

    while len(session['recent_clients']) > cached_results_length:
        session['recent_clients'].pop(last=False)

    values = {
        'clients': results
    }

    return jsonify(values)