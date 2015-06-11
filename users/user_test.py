from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database

from peewee import *

from db import User

import users.user

test_db = SqliteDatabase(':memory:')


class TestUsers(TestCase):

    def run(self, result=None):
        with test_database(test_db, (User,)):
            super(TestUsers, self).run(result)

    def create_test_data(self):
        self._user = users.user.User()
        self._user.create_user('test_name', 'test_password', 'ryan@test.com', 'the_boss', 'what is the answer?', '42',
                               '1234567891', authentication_level=1)

    def test_user_actions(self):
        self.create_test_data()
        self.assertEqual(self._user._user.name, 'test_name')
        self.assertEqual(self._user._user.email, 'ryan@test.com')
        self.assertEqual(self._user._user.title, 'the_boss')
        self.assertEqual(self._user._user.secret_question, 'what is the answer?')
        self.assertEqual(self._user._user.phone_number, '1234567891')
        self.assertEqual(self._user._user.authentication_level, 1)


suite = TestLoader().loadTestsFromTestCase(TestUsers)
TextTestRunner(verbosity=2).run(suite)