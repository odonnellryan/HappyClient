from peewee import IntegerField, Model, TextField, PrimaryKeyField, \
    ForeignKeyField, DecimalField, DateTimeField, SqliteDatabase, PostgresqlDatabase
from bcrypt import gensalt, hashpw
import datetime
import config

if config.debug:
    database = SqliteDatabase('hc.db')
else:
    # eventually put postgres here for production
    pass


class HappyClient(Model):
    class Meta:
        database = database


class Company(HappyClient):
    pk = PrimaryKeyField()
    name = TextField(null=False)
    phone_number = TextField(null=False, default=None)
    address = TextField(null=True, default=None)

    def check_user_authentication(self, user):
        return user.company.pk == self.pk


class User(HappyClient):
    pk = PrimaryKeyField()
    # 1 = owner, 2 = admin, 3 = user
    authentication_level = IntegerField(null=False, default=3)
    name = TextField(null=False, default=None)
    password = TextField(null=True, default=None)
    email = TextField(null=False, default=None)
    title = TextField(null=True, default=None)
    forgot_password = TextField(null=True, default=None)
    secret_question = TextField(null=False, default=None)
    secret_answer = TextField(null=True, default=None)
    phone_number = TextField(null=False, default=None)
    company = ForeignKeyField(Company, related_name='users')

    def validate_secret(self, plaintext_secret_answer):
        plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower().encode('utf-8')
        if hashpw(plaintext_secret_answer, self.secret_answer) == self.secret_answer:
            return True
        return False

    def is_active(self):
        return True

    def get_id(self):
        return self.pk

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def validate_login(self, plaintext_password=None, admin=None):
        if admin:
            if admin.authentication_level == 1 and admin.company.pk == self.company.pk:
                return True
        if plaintext_password:
            try:
                _plaintext_password = plaintext_password.encode('utf-8')
            except AttributeError:
                _plaintext_password = plaintext_password
            if hashpw(_plaintext_password, self.password) == self.password:
                return True
        return False

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        return super(User, self).save(*args, **kwargs)

    def set_secret_answer(self, plaintext_secret_answer):
        plaintext_secret_answer = ("".join(plaintext_secret_answer.split())).lower()
        try:
            plaintext_secret_answer = plaintext_secret_answer.encode('utf-8')
        except AttributeError:
            pass
        self.secret_answer = hashpw(plaintext_secret_answer, gensalt())

    def set_password(self, plaintext_password):
        try:
            plaintext_password = plaintext_password.encode('utf-8')
        except AttributeError:
            pass
        self.password = hashpw(plaintext_password, gensalt())
        return super(User, self).save()


class Client(HappyClient):
    pk = PrimaryKeyField()
    name = TextField(null=False)
    contact_information = TextField(null=True)
    location = TextField(null=True)
    notes = TextField(null=True)
    interaction_reminder_time = DateTimeField(formats='%Y-%m-%d %H:%M', null=True, default=None)
    interaction_reminder_notes = TextField(null=True)
    company = ForeignKeyField(Company, related_name='clients')
    user = ForeignKeyField(User, related_name="clients")

    def save(self, *args, **kwargs):
        try:
            self.interaction_reminder_time = self.interaction_reminder_time.replace(tzinfo=None)
        except TypeError:
            pass
        return super(Client, self).save(*args, **kwargs)

    def safe_get(self, user, *args, **kwargs):
        if self.check_user_authentication(user):
            return super(Client, self).save(*args, **kwargs)
        raise self.DoesNotExist

    def check_user_authentication(self, user):
        return user.company.pk == self.company.pk


class Interaction(HappyClient):
    pk = PrimaryKeyField()
    client = ForeignKeyField(Client, related_name="interactions")
    company = ForeignKeyField(Company, related_name="interactions")
    notes = TextField(null=True)
    # you will rate the interaction 0-5 depending on how well it went
    rating = IntegerField()
    # if a sale was closed you will put in the dollar amount here
    sale = DecimalField(decimal_places=2)
    time = DateTimeField(default=datetime.datetime.now)
    money_owed = DecimalField(decimal_places=2)
    user = ForeignKeyField(User, related_name="interactions")
