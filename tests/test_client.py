# -*- coding: utf-8 -*-

import re
import unittest

from app import create_app, db
from app.models.role import Role
from app.models.user import User


class FalskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Stranger' in response.data)

    def test_register_and_login(self):
        response = self.client.post(
            '/auth/register',
            data={
                'email': 'wills@example.com',
                'username': 'wills',
                'password': 'cat',
                'password2': 'cat'
            }
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.post(
            '/auth/login',
            data={
                'email': 'lewsan@example.com',
                'password': '1vbrcu2',
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(re.search(b'lewsan', response.data))
        self.assertTrue(
            b'You have not confirmed your account yet' in response.data)

        # send a confirmation token
        user = User.query.filter_by(email='wills@example.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get('/auth/confirm/{}'.format(token),
                                   follow_redirects=True)
        user.confirm(token)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            b'You have confirmed your account' in response.data)

        # log out
        response = self.client.get('/auth/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'You have been logged out' in response.data)
