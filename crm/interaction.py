import db
from exceptions import InteractionInvalid


class Interaction:
    def __init__(self, interaction_pk=None, user=None):
        if interaction_pk and user:
            try:
                self.data = (db.Interaction.select()
                             .where(db.Interaction.pk == interaction_pk)
                             .where(db.Interaction.company.pk == user.data.company.pk)
                             .get())
            except db.Interaction.DoesNotExist:
                raise InteractionInvalid
        else:
            self.data = None

    def create_interaction(self, user, client, rating, sale, money_owed, notes=None):
        if not self.data and (client.data in self.data.user.clients):
            self.data = db.Interaction.create(client=client.data, company=client.data.company, rating=rating,
                                              sale=sale, money_owed=money_owed, notes=notes, user=user.data)
            return True

    def delete(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise InteractionInvalid("Cannot modify invalid interaction.")

    def check_user_authentication(self, user):
        return user.data.company.pk == self.data.company.pk

    def change_information(self, client=None, rating=None, sale=None, money_owed=None, notes=None,
                           user=None):
        if client:
            if client.data in self.data.user.clients:
                self.data.client = client.data
        if rating:
            self.data.rating = rating
        if sale:
            self.data.sale = sale
        if money_owed:
            self.data.money_owed = money_owed
        if notes:
            self.data.notes = notes
        if user and user.data.company.pk == self.data.company.pk:
            self.data.user = user

        return self.data.save()
