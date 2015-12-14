from flask import Blueprint, render_template, request, flash, session, redirect, url_for, g
from flask_login import current_user
from db import Interaction
from views.forms import InteractionForm
from utilities import flashed_errors, helper_functions
interaction = Blueprint('interaction', __name__, url_prefix='/interaction')

get_client = helper_functions.get_client

@interaction.route('/new/<int:client_pk>/', methods=['GET', 'POST'])
def new(client_pk=None):
    client = get_client(client_pk, company=g.company)
    if not client:
        flash(flashed_errors.CLIENT_DOESNT_EXIST)
        return redirect(url_for('company.home'))
    form = InteractionForm(request.form)
    if current_user.is_authenticated():
        user = current_user.pk
    else:
        user = None
    if request.method == 'POST' and form.add_interaction.data and form.validate():
        client = Interaction().create(client=client.pk, company=g.company.pk, notes=form.interaction_reminder_notes.data,
                                      rating=form.rating.data, sale=form.sale.data, time=form.interaction_reminder_time.data,
                                      user=user)
        return redirect(url_for('interaction.home', client_pk=client.pk))
    return render_template('interaction/new.html', form=form, client=client)


@interaction.route('/edit/<int:interaction_pk>/')
@interaction.route('/edit/', methods=['GET', 'POST'])
def edit(interaction_pk=None):
    """
    edits the company information
    :return:
    """
    if not interaction_pk:
        redirect(url_for('client.home'))
    try:
        interaction = Interaction().get(Interaction.pk == interaction_pk)
        if not interaction.check_user_authentication(current_user, company=g.company):
            flash(flashed_errors.INTERACTION_ERROR)
            return redirect(url_for('company.home'))
    except Interaction.DoesNotExist:
        flash(flashed_errors.INTERACTION_ERROR)
        return redirect(url_for('company.home'))
    form = InteractionForm(request.form)
    form.interaction_reminder_notes.data = interaction.notes
    form.interaction_reminder_time.data = interaction.time
    form.rating.data = interaction.rating
    form.sale.data = interaction.sale

    if request.method == 'POST' and form.validate():
        query = interaction.update(notes=form.interaction_reminder_notes.data, time=form.interaction_reminder_time.data,
                                   rating=form.rating.data, sale=form.sale.data)
        query.execute()

    return render_template('interaction/edit.html', form=form)