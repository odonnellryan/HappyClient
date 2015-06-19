import db, exceptions

class Company:
    def __init__(self, company_pk=None, user=None):
        if company_pk and user:
            try:
                self.data = db.Company.select.where(db.Company.pk == company_pk)
            except db.Company.DoesNotExist:
                raise exceptions.CompanyInvalid
            if self.check_user_authentication(user):
                pass
            else:
                self.data = None
        else:
            self.data = None

    def create_company(self, name, phone_number, address=None):
        if not self.data:
            self.data = db.Company.create(name=name, phone_number=phone_number, address=address)

    def delete(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise exceptions.CompanyInvalid

    def check_user_authentication(self, user):
        return user.data.company.pk == self.data.pk

    def change_information(self, phone_number=None, address=None, name=None):
        if address:
            self.data.name = name
        if phone_number:
            self.data.phone_number = phone_number
        if name:
            self.data.name = name
        return self.data.save()