import db, exceptions

class Company:
    def __init__(self, company_pk=None):
        if company_pk:
            try:
                self.data = db.Company.select.where(db.Company.pk == company_pk)
            except db.Company.DoesNotExist:
                raise exceptions.CompanyInvalid
        else:
            self.data = None

    def create_company(self, name, phone_number, address=None):
        if not self.data:
            self.data = db.Company.create(name=name, phone_number=phone_number, address=address)

    def delete(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise exceptions.UserInvalid

    def check_user_authentication(self, user):
        try:
            company = (db.Company
                        .select()
                        .join(db.UserCompany)
                        .join(db.User)
                        .where(db.Company.pk == self.data.pk)
                        #.switch(db.User)
                        .where(db.User.pk == user.pk)
                        .get())
            if company:
                return True
        except db.Company.DoesNotExist:
                return False



    def change_information(self, phone_number=None, address=None, name=None):
        if address:
            self.data.name = name
        if phone_number:
            self.data.phone_number = phone_number
        if name:
            self.data.name = name
        return self.data.save()