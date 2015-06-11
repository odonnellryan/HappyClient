import db, peewee, exceptions
from bcrypt import gensalt, hashpw


class User:

    def __init__(self, user_pk=None, email=None):
        super().__init__()
        if user_pk:
            try:
                self._user = db.User.select().where(db.User.pk == user_pk).get()
            except db.User.DoesNotExist:
                raise exceptions.UserInvalid

        elif email:
            email = email.strip().lower()
            try:
                self._user = db.User.select().where(db.User.email == email).get()
            except peewee.DoesNotExist as e:
                raise exceptions.UserInvalid(e)
        else:
            self._user = None

    def create_user(self, name, plaintext_password, email, title, secret_question, plaintext_secret_answer,
                    phone_number, authentication_level=None):
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
            self._user = db.User.create(authentication_level=authentication_level, name=name,
                                        password=password, email=email, title=title, secret_question=secret_question,
                                        secret_answer=secret_answer, phone_number=phone_number)

    def delete(self):
        if self._user:
            return self._user.delete()
        else:
            raise exceptions.UserInvalid

    def validate_login(self, plaintext_password):
        if self._user:
            if hashpw(plaintext_password.encode('utf-8'), self._user.password) == self._user.password:
                return True
            else:
                return False

    def validate_secret(self, plaintext_secret_answer):
        if self._user:
            plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower().encode('utf-8')
            if hashpw(plaintext_secret_answer, self._user.secret_answer) == self._user.secret_answer:
                return True
            else:
                return False

    def change_information(self, plaintext_password, authentication_level=None, name=None, email=None, title=None,
                           secret_question=None, plaintext_secret_answer=None, phone_number=None,
                           new_plaintext_password=None):
        if self.validate_login(plaintext_password):
            if authentication_level:
                self._user.authentication_level = authentication_level
            if new_plaintext_password:
                self._user.password = hashpw(new_plaintext_password.encode('utf-8'), gensalt())
            if name:
                self._user.name = name
            if email:
                self._user.email = email
            if title:
                self._user.title = title
            if secret_question and plaintext_secret_answer:
                self._user.secret_question = secret_question
                plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower().encode('utf-8')
                self._user.secret_answer = hashpw(plaintext_secret_answer, gensalt())
            if phone_number:
                self._user.phone_number = phone_number
            self._user.save()