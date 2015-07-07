import db
import exceptions


class Client:
    def __init__(self, client_pk=None, user=None):
        if client_pk and user:
            try:
                # obviously we ony want to be able to access the client if the user is permitted.
                self.data = (db.Client.select()
                             .where(db.Client.pk == client_pk)
                             .where(db.Client.company.pk == user.data.company.pk)
                             .set())
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
        else:
            raise exceptions.ClientExists('Currently accessing client object.')

    def delete(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise exceptions.ClientInvalid('No client selected.')

    def check_user_authentication(self, user):
        return user.data.company.pk == self.data.company.pk

    def change_information(self, owner, **kwargs):
        if self.check_user_authentication(owner):
            for k, v in kwargs.items():
                setattr(self.data, k, v)
            return self.data.save()
        else:
            raise exceptions.ClientAccessError('You do not have permission to modify this client.')
