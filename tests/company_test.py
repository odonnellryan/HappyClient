from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database
from peewee import *

from db import Company, User

test_db = SqliteDatabase(':memory:')
class TestCompanies(TestCase):

    # this override makes it so we don't need to use the context manager for each call
    def run(self, result=None):
        with test_database(test_db, (Company, User)):
            super(TestCompanies, self).run(result)

    def create_test_data(self):
        self._company = Company().create(name='test_name', phone_number='1223456789',
                                         address='123 test road, testville test')

    def test_company_creation(self):
        self.create_test_data()
        self.assertEqual(self._company.name, 'test_name')
        self.assertEqual(self._company.phone_number, '1223456789')
        self.assertEqual(self._company.address, '123 test road, testville test')

    def test_company_authentication(self):
        self.create_test_data()
        _user = User().create(name='test_name', email='ryan@test.com', title='the_boss',
                          secret_question='what is the answer?',
                            phone_number='1234567891', authentication_level=3, company=self._company.pk)
        self.assertTrue(self._company.check_user_authentication(_user))
        _other_company = Company().create(name='test_name', phone_number='1223456789',
                                         address='123 test road, testville test')
        self.assertNotEqual(_other_company.pk, self._company.pk)
        self.assertFalse(_other_company.check_user_authentication(_user))

    def test_get_company(self):
        self.create_test_data()
        _user = User().create(name='test_name', email='ryan@test.com', title='the_boss',
                          secret_question='what is the answer?',
                            phone_number='1234567891', authentication_level=3, company=self._company.pk)
        _other_company = Company().create(name='test_name', phone_number='1223456789',
                                         address='123 test road, testville test')
        self.assertFalse((_other_company.pk == _user.company.pk))
        _other_user = User().create(name='test_name', email='ryan@test.com', title='the_boss',
                          secret_question='what is the answer?',
                            phone_number='1234567891', authentication_level=3, company=_other_company.pk)
        self.assertEqual(_other_company.pk, _other_user.company.pk)

    def test_change_information(self):
        self.create_test_data()
        query = (Company().update(name="testing_name", phone_number="9999999999", address="test_location")
            .where(Company.pk == self._company.pk))
        query.execute()
        _test_company = Company().get(Company.pk == self._company.pk)
        self.assertEqual(_test_company.name, "testing_name")
        self.assertEqual(_test_company.phone_number, "9999999999")
        self.assertEqual(_test_company.address, "test_location")