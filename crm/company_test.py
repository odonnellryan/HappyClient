from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database

from peewee import *

from db import Company, User

import users.user as user
import crm.company as company
import exceptions

test_db = SqliteDatabase(':memory:')
class TestCompanies(TestCase):

    # this override makes it so we don't need to use the context manager for each call
    def run(self, result=None):
        with test_database(test_db, (Company, User)):
            super(TestCompanies, self).run(result)

    def create_test_data(self):
        self._company = company.Company()
        self._company.create_company('test_name', '1223456789', '123 test road, testville test')

    def test_company_creation(self):
        self.create_test_data()
        self.assertEqual(self._company.data.name, 'test_name')
        self.assertEqual(self._company.data.phone_number, '1223456789')
        self.assertEqual(self._company.data.address, '123 test road, testville test')

    def test_company_authentication(self):
        _user = user.User()
        _user.create_user('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1)
        self.create_test_data()


suite = TestLoader().loadTestsFromTestCase(TestCompanies)
TextTestRunner(verbosity=2).run(suite)