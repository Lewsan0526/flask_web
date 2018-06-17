# -*- coding: utf-8 -*-

import unittest
from app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        user = User(password='cat')
        self.assertTrue(user.password is not None)

    def test_no_password_getter(self):
        user = User(password='cat')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='cat')
        self.assertTrue(user.verify_password('cat'))
        self.assertFalse(user.verify_password('dog'))

    def test_password_salts_are_random(self):
        user_1 = User(password='cat')
        user_2 = User(password='cat')
        self.assertTrue(user_1.password == user_2.password)
