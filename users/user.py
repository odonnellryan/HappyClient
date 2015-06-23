import db, peewee, exceptions
from bcrypt import gensalt, hashpw

class User:

    """

        This is the class that owns the user object.
        User data is stored in self.data.
        This is used by both the user and by admins (users will of course need to authenticate)


    """

    def __init__(self, plaintext_password=None, user_pk=None, email=None, admin=None):
        if user_pk and (plaintext_password or admin):
            try:
                self.data = db.User.select().where(db.User.pk == user_pk).get()
            except db.User.DoesNotExist as e:
                raise exceptions.UserInvalid(e)
        elif email and (plaintext_password or admin):
            email = email.strip().lower()
            try:
                self.data = db.User.select().where(db.User.email == email).get()
            except peewee.DoesNotExist as e:
                raise exceptions.UserInvalid(e)
        else:
            self.data = None

        if self.data:
            if not self.validate_login(plaintext_password=plaintext_password, admin=admin):
                self.data = None

    def create_user(self, name, plaintext_password, email, title, secret_question, plaintext_secret_answer,
                    phone_number, company, authentication_level=None):
        email = email.strip().lower()
        try:
            _user = db.User.select().where(db.User.email == email).get()
            if _user:
                raise exceptions.UserExists
        except db.User.DoesNotExist:
            # properly hash our things
            password = hashpw(plaintext_password.encode('utf-8'), gensalt())
            # removes all whitespace and sets it to lower
            # a little less secure, but this is meant as an extra security measure to begin with
            # the reset link will still be emailed to the user.
            plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower().encode('utf-8')
            secret_answer = hashpw(plaintext_secret_answer, gensalt())
            # auth level of 3 is a basic user, default level.
            if not authentication_level:
                authentication_level = 3

            self.data = db.User.create(authentication_level=authentication_level, name=name,
                                        password=password, email=email, title=title, secret_question=secret_question,
                                        secret_answer=secret_answer, phone_number=phone_number, company=company.data)

    def delete_user(self):
        if self.data:
            return self.data.delete_instance()
        else:
            raise exceptions.UserInvalid

    def validate_secret(self, plaintext_secret_answer):
        if self.data:
            plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower().encode('utf-8')
            if hashpw(plaintext_secret_answer, self.data.secret_answer) == self.data.secret_answer:
                return True
        return False

    def validate_login(self, plaintext_password=None, admin=None):
        if admin:
            if admin.data.authentication_level == 1 and admin.data.company.pk == self.data.company.pk:
                return True
        if plaintext_password:
            try:
                _plaintext_password = plaintext_password.encode('utf-8')
            except: _plaintext_password = plaintext_password
            try:
                _hash = self.data.password.encode('utf-8')
            except: _hash = self.data.password
            if hashpw(_plaintext_password, _hash) == _hash:
                return True
        return False

    def change_information(self, plaintext_password=None, admin=None, authentication_level=None, name=None, email=None, title=None,
                           secret_question=None, plaintext_secret_answer=None, phone_number=None,
                           new_plaintext_password=None):
        if self.validate_login(plaintext_password=plaintext_password, admin=admin):
            if authentication_level:
                self.data.authentication_level = authentication_level
            if new_plaintext_password:
                self.data.password = hashpw(new_plaintext_password.encode('utf-8'), gensalt())
            if name:
                self.data.name = name
            if email:
                self.data.email = email
            if title:
                self.data.title = title
            if secret_question and plaintext_secret_answer:
                self.data.secret_question = secret_question
                plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower().encode('utf-8')
                self.data.secret_answer = hashpw(plaintext_secret_answer, gensalt())
            if phone_number:
                self.data.phone_number = phone_number
            self.data.save()

    def get_company(self):
        return self.data.company