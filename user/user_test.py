from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database

from peewee import *

from db import User, Company

import user.user as user
import crm.company as company
import exceptions

test_db = SqliteDatabase(':memory:')


class TestUsers(TestCase):

    # this override makes it so we don't need to use the context manager for each call
    def run(self, result=None):
        with test_database(test_db, (User, Company)):
            super(TestUsers, self).run(result)

    def create_test_data(self):
        self._user = user.User()
        self._company = company.Company()
        self._company.create_company('test_name', '1223456789', '123 test road, testville test')
        self._user.create('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=3, company=self._company)
        self._admin = user.User()
        self._admin.create('admin', 'test_password', 'admin@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1, company=self._company)

    def test_user_creation(self):
        self.create_test_data()
        self.assertEqual(self._user.data.name, 'test_name')
        self.assertEqual(self._user.data.email, 'ryan@test.com')
        self.assertEqual(self._user.data.title, 'the_boss')
        self.assertEqual(self._user.data.secret_question, 'what is the answer?')
        self.assertEqual(self._user.data.phone_number, '1234567891')
        self.assertEqual(self._user.data.authentication_level, 3)

    def test_user_delete(self):
        self.create_test_data()
        deleted = self._user.delete()
        self.assertEqual(deleted, 1)

    def test_user_validation(self):
        self.create_test_data()
        self.assertTrue(self._user.validate_login(plaintext_password='test_password'))

    def test_user_secret_question(self):
        self.create_test_data()
        self.assertTrue(self._user.validate_secret('42'))
        self.assertTrue(self._user.validate_secret('  42  '))
        self.assertFalse(self._user.validate_secret('  forty-two  '))

    def test_user_change_info(self):
        self.create_test_data()
        self._user.change_information('test_password', authentication_level=2, email='test@email.com',
                                      phone_number='1231231234', name='new_name', title='new_title')
        pk = self._user.data.pk
        self._user_2 = user.User(user_pk=pk, admin=self._admin)
        self.assertEqual(self._user_2.data.authentication_level, 2)
        self.assertEqual(self._user_2.data.phone_number, '1231231234')
        self.assertEqual(self._user_2.data.name, 'new_name')
        self.assertEqual(self._user_2.data.title, 'new_title')

    def test_user_change_password(self):
        self.create_test_data()
        self._user.change_information('test_password', new_plaintext_password='new_password')

        self.assertFalse(self._user.validate_login(plaintext_password='test_password'))
        self.assertTrue(self._user.validate_login(plaintext_password='new_password'))

    def test_user_change_secret_question(self):
        self.create_test_data()
        self._user.change_information('test_password', secret_question='new_question',
                                      plaintext_secret_answer='new answer')
        self.assertFalse(self._user.validate_secret('test_password'))
        self.assertTrue(self._user.validate_secret('new answer'))
        self.assertTrue(self._user.validate_secret('newanswer'))

    def test_get_user_by_pk(self):
        self.create_test_data()
        pk_1 = self._user.data.pk
        _user = user.User(user_pk=pk_1)
        self.assertIsNone(_user.data)
        _user3 = user.User(user_pk=pk_1, plaintext_password='test_password')
        pk_2 = _user3.data.pk
        self.assertEqual(pk_1, pk_2)
        #self.assertRaises(exceptions.UserInvalid, user.User, user_pk=1000, plaintext_password='test_password')

    def test_get_user_by_email(self):
        self.create_test_data()
        email = 'ryan@test.com'
        # need password to get user, this should be none
        _user_1 = user.User(email=email)
        self.assertIsNone(_user_1.data)
        _user_12 = user.User(email=email, plaintext_password='test_password')
        self.assertEqual(_user_12.data.pk, self._user.data.pk)
        # should raise an exception.
        #self.assertRaises(exceptions.UserInvalid, user.User, email='doesnotexist@test.com',
#                          plaintext_password='test_password')

    def test_get_company(self):
        self.create_test_data()
        self.assertEqual(self._company.data.pk, self._user.data.company.pk)

suite = TestLoader().loadTestsFromTestCase(TestUsers)
TextTestRunner(verbosity=2).run(suite)