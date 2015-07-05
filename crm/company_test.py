from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database
import exceptions
from peewee import *

from db import Company, User

import user.user as user
import crm.company as company

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
        self.create_test_data()
        _user = user.User()
        _user.create('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1, company=self._company)
        self.assertTrue(self._company.check_user_authentication(_user))
        _other_company = company.Company()
        _other_company.create_company('test_name2', '12234567893', '123 test road4, testville test')
        self.assertNotEqual(_other_company.data.pk, self._company.data.pk)
        self.assertFalse(_other_company.check_user_authentication(_user))

    def test_get_company(self):
        self.create_test_data()
        _user = user.User()
        _user.create('test_nam4545e3', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1, company=self._company)
        _other_company = company.Company()
        _other_company.create_company('test_name2', '12234567893', '123 test road4, testville test')
        self.assertFalse((_other_company.data == _user.data.company))
        _other_user = user.User()
        _other_user.create('testame34', 'test_password', 'ryan3@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1, company=_other_company)
        self.assertEqual(_other_company.data.pk, _other_user.data.company.pk)
        _test_company = company.Company(user=_other_user)
        self.assertEqual(_test_company.data.pk, _other_company.data.pk)

    def test_change_information(self):
        self.create_test_data()
        _user = user.User()
        _user.create('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1, company=self._company)
        self._company.change_information(_user, name="testing_name", phone_number="9999999999", address="test_location")
        _test_company = company.Company(user=_user)
        self.assertEqual(_test_company.data.name, "testing_name")
        self.assertEqual(_test_company.data.phone_number, "9999999999")
        self.assertEqual(_test_company.data.address, "test_location")





suite = TestLoader().loadTestsFromTestCase(TestCompanies)
TextTestRunner(verbosity=2).run(suite)