import db, exceptions

class Company:
    def __init__(self, user=None):
        if user:
            try:
                self.data = db.Company.select().where(db.Company.pk == user.data.company.pk).get()
            except db.Company.DoesNotExist:
                raise exceptions.CompanyInvalid
        else:
            self.data = None

    def create_company(self, name, phone_number, address=None):
        if not self.data:
            self.data = db.Company.create(name=name, phone_number=phone_number, address=address)
        else:
            raise(exceptions.CompanyExists)

    def delete(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise exceptions.CompanyInvalid

    def check_user_authentication(self, user):
        return user.data.company.pk == self.data.pk

    def change_information(self, user, **kwargs):
        # this method of setting the attributes may not always work as intended.
        # specifically, it does not check if the attribute exists or not.
        # but this is simple enough to be OK
        if self.check_user_authentication(user):
            for k, v in kwargs.items():
                setattr(self.data, k, v)
            return self.data.save()
        raise exceptions.CompanyAccessError("You are not permitted to modify company information.")