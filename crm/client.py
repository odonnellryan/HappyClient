import db, exceptions

class Client:
    def __init__(self, client_pk=None, user=None):
        if client_pk and user:
            try:
                self.data = (db.Client.select.where(db.Client.pk == client_pk)
                             .where(db.Client.company.pk == user.data.company.pk))
            except db.Client.DoesNotExist:
                raise exceptions.ClientInvalid
        else:
            self.data = None

    def create_client(self, user, name, contact_information, interaction_reminder_time=None,
                      interaction_reminder_notes=None, location=None, notes=None):
        if not self.data:
            self.data = db.Client.create(name=name, contact_information=contact_information, location=location,
                                         notes=notes, interaction_reminder_notes=interaction_reminder_notes,
                                         interaction_reminder_time=interaction_reminder_time,
                                         company=user.data.company, user=user.data)
            return True
        return False

    def delete(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise exceptions.UserInvalid

    def check_user_authentication(self, user):
        return user.data.company.pk == self.data.company.pk

    def change_information(self, owner, user=None, name=None, contact_information=None, interaction_reminder_time=None,
                      interaction_reminder_notes=None, location=None, notes=None):
        if user:
            if owner.data.pk == user.data.:
                self.data.client = client.data
        if rating:
            self.data.rating = rating
        if sale:
            self.data.sale = sale
        if money_owed:
            self.data.money_owed = money_owed
        if notes:
            self.data.notes = notes

        return self.data.save()