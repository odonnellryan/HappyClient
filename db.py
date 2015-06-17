from peewee import IntegerField, Model, TextField, PrimaryKeyField, \
    PostgresqlDatabase, ForeignKeyField, DecimalField, DateTimeField
import config

database = PostgresqlDatabase(config.database['database'], user=config.database['username'],
                              passwd=config.database['password'])


class HappyClient(Model):
    class Meta:
        database = database


class Company(HappyClient):
    pk = PrimaryKeyField()
    name = TextField(null=False)
    phone_number = TextField(null=False, default=None)
    address = TextField(null=True, default=None)


class User(HappyClient):
    pk = PrimaryKeyField()
    # 1 = owner, 2 = admin, 3 = user
    authentication_level = IntegerField(null=False, default=3)
    name = TextField(null=False, default=None)
    password = TextField(null=False, default=None)
    email = TextField(null=False, default=None)
    title = TextField(null=True, default=None)
    forgot_password = TextField(null=True, default=None)
    secret_question = TextField(null=False, default=None)
    secret_answer = TextField(null=False, default=None)
    phone_number = TextField(null=False, default=None)


class UserCompany(HappyClient):
    company = ForeignKeyField(Company, related_name='companies')
    user = ForeignKeyField(User, related_name='users')


class Client(HappyClient):
    pk = PrimaryKeyField()
    name = TextField(null=False)
    contact_information = TextField(null=False)
    location = TextField(null=True)
    notes = TextField(null=True)
    interaction_reminder = DateTimeField(formats='%Y-%m-%d %H:%M')


class Interaction(HappyClient):
    pk = PrimaryKeyField()
    client = ForeignKeyField(Client, related_name="interactions")
    notes = TextField(null=True)
    # you will rate the interaction 0-5 depending on how well it went
    rating = IntegerField()
    # if a sale was closed you will put in the dollar amount here
    sale = DecimalField(decimal_places=2)
    time = DateTimeField(formats='%Y-%m-%d %H:%M')
    money_owed = DecimalField(decimal_places=2)
