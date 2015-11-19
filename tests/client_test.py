import unittest
from playhouse.test_utils import test_database
# import exceptions
from peewee import *

from db import Company, User, Client

test_db = SqliteDatabase(':memory:')


class TestClients(unittest.TestCase):
    # this override makes it so we don't need to use the context manager for each call
    def run(self, result=None):
        with test_database(test_db, (Client, Company, User)):
            super(TestClients, self).run(result)

    def create_test_data(self):
        self._company = Company().create(name='test_name', phone_number='1223456789',
                                         address='123 test road, testville test')
        self._user = User().create(name='test_name', email='ryan@test.com', title='the_boss',
                          secret_question='what is the answer?',
                            phone_number='1234567891', authentication_level=3, company=self._company.pk)
        self._client = Client().create(user=self._user.pk, name="test_client", contact_information="contact info",
                                       company=self._company.pk)

    def test_client_creation(self):
        self.create_test_data()
        self.assertEqual(self._client.name, 'test_client')
        self.assertEqual(self._client.contact_information, 'contact info')

    def test_client_authentication(self):
        self.assertTrue(self._client.check_user_authentication(self._user))