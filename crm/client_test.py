import unittest
from playhouse.test_utils import test_database
# import exceptions
from peewee import *

from db import Company, User, Client

import user.user as user
import crm.company as company
import crm.client as client

test_db = SqliteDatabase(':memory:')


class TestClients(unittest.TestCase):
    # this override makes it so we don't need to use the context manager for each call
    def run(self, result=None):
        with test_database(test_db, (Client, Company, User)):
            super(TestClients, self).run(result)

    def create_test_data(self):
        self._company = company.Company()
        self._company.create_company('test_name2', '12234567893', '123 test road4, testville test')
        self._user = user.User()
        self._user.create_user('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                          '1234567891', authentication_level=1, company=self._company)
        self._client = client.Client()
        self._client.create_client(self._user, "test_client", "contact info")

    def test_client_creation(self):
        self.create_test_data()
        self.assertEqual(self._client.data.name, 'test_client')
        self.assertEqual(self._client.data.contact_information, 'contact info')

    def test_client_authentication(self):
        self.fail("Not yet implemented")

    def test_get_client(self):
        self.fail("Not yet implemented")

    def test_change_information(self):
        self.fail("Not yet implemented")


suite = unittest.TestLoader().loadTestsFromTestCase(TestClients)
unittest.TextTestRunner(verbosity=2).run(suite)
