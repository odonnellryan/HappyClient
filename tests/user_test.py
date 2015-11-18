from unittest import TestCase, TestLoader, TextTestRunner
from playhouse.test_utils import test_database

from peewee import *
from db import User, Company

test_db = SqliteDatabase(':memory:')


class TestUsers(TestCase):
    def run(self, result=None):
        with test_database(test_db, (User, Company)):
            super(TestUsers, self).run(result)

    def create_test_data(self):
        self._company = Company().create(name='test_name', phone_number='1223456789', address='123 test road, testville test')
        self._user = User().create(name='test_name', email='ryan@test.com', title='the_boss',
                          secret_question='what is the answer?',
                            phone_number='1234567891', authentication_level=3, company=self._company.pk)
        self._user.set_password('test_password')
        self._user.set_secret_answer('42')
        self._admin = User().create(name='admin', email='admin@test.com', title='the_boss',
                           secret_question='what is the answer?',
                               phone_number='1234567891', authentication_level=1, company=self._company.pk)
        self._admin.set_password('test_password')
        self._admin.set_secret_answer('42')

    def test_user_creation(self):
        self.create_test_data()
        self.assertEqual(self._user.name, 'test_name')
        self.assertEqual(self._user.email, 'ryan@test.com')
        self.assertEqual(self._user.title, 'the_boss')
        self.assertEqual(self._user.secret_question, 'what is the answer?')
        self.assertEqual(self._user.phone_number, '1234567891')
        self.assertEqual(self._user.authentication_level, 3)

    def test_user_delete(self):
        self.create_test_data()
        deleted = self._user.delete()
        self.assertEqual(deleted, 1)

    def test_user_validation(self):
        self.create_test_data()
        self.assertTrue(self._user.validate_login(plaintext_password='test_password'))

    def test_user_validation_after_update(self):
        self.create_test_data()
        test_name = "test_name"

        self.assertTrue(self._user.validate_login(plaintext_password='test_password'))

    def test_user_secret_question(self):
        self.create_test_data()
        self.assertTrue(self._user.validate_secret('42'))
        self.assertTrue(self._user.validate_secret('  42  '))
        self.assertFalse(self._user.validate_secret('  forty-two  '))

    def test_user_change_info(self):
        self.create_test_data()
        query = User().update(authentication_level=2, email='test@email.com',
                                      phone_number='1231231234', name='new_name', title='new_title').where(User.pk == self._user.pk)
        query.execute()
        pk = self._user.pk
        self._user_2 = User().get(pk=pk)
        self.assertEqual(self._user_2.authentication_level, 2)
        self.assertEqual(self._user_2.phone_number, '1231231234')
        self.assertEqual(self._user_2.name, 'new_name')
        self.assertEqual(self._user_2.title, 'new_title')

    def test_user_change_password(self):
        self.create_test_data()
        self._user.set_password('new_password')
        self.assertFalse(self._user.validate_login(plaintext_password='test_password'))
        self.assertTrue(self._user.validate_login(plaintext_password='new_password'))

    def test_user_change_secret_question(self):
        self.create_test_data()
        self._user.set_secret_answer('neW Answer')
        self.assertFalse(self._user.validate_secret('test_password'))
        self.assertTrue(self._user.validate_secret('new answer'))
        self.assertTrue(self._user.validate_secret('newanswer'))

    def test_get_user_by_pk(self):
        self.create_test_data()
        pk_1 = self._user.pk
        _user = User().get(pk=pk_1)
        self.assertIsNotNone(_user)
        _user3 = User().get(pk=pk_1)
        pk_2 = _user3.pk
        self.assertEqual(pk_1, pk_2)

    def test_get_user_by_email(self):
        self.create_test_data()
        email = 'ryan@test.com'
        _user_1 = User().get(email=email)
        self.assertIsNotNone(_user_1)
        _user_2 = User().get(email=email)
        self.assertEqual(_user_2.pk, self._user.pk)

    def test_get_company(self):
        self.create_test_data()
        self.assertEqual(self._company.pk, self._user.company.pk)