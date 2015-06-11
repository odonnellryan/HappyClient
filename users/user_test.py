from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database

from peewee import *

from db import User

import users.user
import exceptions

test_db = SqliteDatabase(':memory:')


class TestUsers(TestCase):

    # this override makes it so we don't need to use the context manager for each call
    def run(self, result=None):
        with test_database(test_db, (User,)):
            super(TestUsers, self).run(result)

    def create_test_data(self):
        self._user = users.user.User()
        self._user.create_user('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1)

    def test_user_creation(self):
        self.create_test_data()
        self.assertEqual(self._user._user.name, 'test_name')
        self.assertEqual(self._user._user.email, 'ryan@test.com')
        self.assertEqual(self._user._user.title, 'the_boss')
        self.assertEqual(self._user._user.secret_question, 'what is the answer?')
        self.assertEqual(self._user._user.phone_number, '1234567891')
        self.assertEqual(self._user._user.authentication_level, 1)

    def test_user_delete(self):
        deleted = self._user.delete()
        self.assertEqual(deleted, 1)
        self._user.delete()

    def test_user_validation(self):
        self.create_test_data()
        self.assertTrue(self._user.validate_login('test_password'))

    def test_user_secret_question(self):
        self.create_test_data()
        self.assertTrue(self._user.validate_secret('42'))
        self.assertTrue(self._user.validate_secret('  42  '))
        self.assertFalse(self._user.validate_secret('  forty-two  '))

    def test_user_change_info(self):
        self.create_test_data()
        self._user.change_information('test_password', authentication_level=2, email='test@email.com',
                                      phone_number='1231231234', name='new_name', title='new_title')
        pk = self._user._user.pk
        self._user_2 = users.user.User(user_pk=pk)
        self.assertEqual(self._user_2._user.authentication_level, 2)
        self.assertEqual(self._user_2._user.phone_number, '1231231234')
        self.assertEqual(self._user_2._user.name, 'new_name')
        self.assertEqual(self._user_2._user.title, 'new_title')

    def test_user_change_password(self):
        self.create_test_data()
        self._user.change_information('test_password', new_plaintext_password='new_password')
        self.assertFalse(self._user.validate_login('test_password'))
        self.assertTrue(self._user.validate_login('new_password'))

    def test_user_change_secret_question(self):
        self.create_test_data()
        self._user.change_information('test_password', secret_question='new_question',
                                      plaintext_secret_answer='new answer')
        self.assertFalse(self._user.validate_secret('test_password'))
        self.assertTrue(self._user.validate_secret('new answer'))
        self.assertTrue(self._user.validate_secret('newanswer'))

    def test_get_user_by_pk(self):
        self.create_test_data()
        pk_1 = self._user._user.pk
        self._user_1 = users.user.User(user_pk=pk_1)
        pk_2 = self._user_1._user.pk
        self.assertEqual(pk_1, pk_2)
        self.assertRaises(exceptions.UserInvalid, users.user.User, user_pk=1000)

    def test_get_user_by_email(self):
        self.create_test_data()
        email = 'ryan@test.com'
        self._user_1 = users.user.User(email=email)
        # should raise an exception.
        self.assertRaises(exceptions.UserInvalid, users.user.User, email='doesnotexist@test.com')


suite = TestLoader().loadTestsFromTestCase(TestUsers)
TextTestRunner(verbosity=2).run(suite)