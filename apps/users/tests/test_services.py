import json
import os

from django.test import (
    TestCase,
)

from users.models import CustomUser
from users.services import (
    create_and_return_user,
    is_user_logged_in,
    register_user,
    login_user,
    confirm_email,
    settings_user,
    password_reset_request,
    password_reset_get,
    password_reset_post,
    get_user,
    profile_post,
)


CUR_DIR = os.path.dirname(__file__)


class ServiceTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.path = f'{CUR_DIR}/fixtures/services'

        cls.user = CustomUser.objects.create_user(
            email="test1@example.com",
            username="test1",
            password="password123",
            url_hash="ddf7d051-84f6-4a04-a973-f4f57672d8d7",
        )

    def test_create_and_return_user(self):
        path = f'{self.path}/create_and_return_user'
        response = self.client.get('/')
        request = response.wsgi_request

        fixtures = (
            (200, 'valid',),
            (500, 'user_exists',),
            (500, 'invalid',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code, user = create_and_return_user(
                request=request,
                data=data,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_is_user_logged_in(self):
        path = f'{self.path}/is_user_logged_in'
        response = self.client.get('/')
        request = response.wsgi_request

        fixtures = (
            (200, 'valid',),
            (401, 'not_auth',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code = is_user_logged_in(
                request=request,
                data=data,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_register_user(self):
        path = f'{self.path}/register_user'
        fixtures = (
            (200, 'valid',),
            (400, 'invalid',),
            (400, 'required_username',),
            (400, 'user_exists',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
            )
            request = response.wsgi_request

            status_code = register_user(
                request=request,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_login_user(self):
        path = f'{self.path}/login_user'
        fixtures = (
            (200, 'valid',),
            (400, 'invalid',),
            (400, 'required_password',),
            (401, 'not_auth',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
            )
            request = response.wsgi_request

            status_code = login_user(
                request=request,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_confirm_email(self):
        path = f'{self.path}/confirm_email'
        fixtures = (
            (200, 'valid',),
            (404, 'not_found',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                url_hash = json.load(file)

            response = self.client.get(path='/')
            request = response.wsgi_request

            status_code = confirm_email(
                request=request,
                url_hash=url_hash,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_settings_user(self): # search
        path = f'{self.path}/settings_user'

        fixtures = (
            (400, 'invalid',),
            (400, 'passwords_mismatch',),
            (200, 'valid',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            self.client.login(
                email='test1@example.com',
                password='password123',
            )

            response = self.client.post(
                path='/',
                data=data,
            )

            request = response.wsgi_request

            status_code = settings_user(
                request=request,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_password_reset_request(self):
        path = f'{self.path}/password_reset_request'

        fixtures = (
            (200, 'valid',),
            (400, 'invalid',),
            (400, 'required_email',),
            (404, 'not_found',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
            )

            request = response.wsgi_request

            status_code = password_reset_request(
                request=request,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_password_reset_get(self):
        path = f'{self.path}/password_reset_get'

        fixtures = (
            (200, 'valid',),
            (404, 'not_found',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                url_hash = json.load(file)

            response = self.client.get(path='/')

            request = response.wsgi_request

            status_code = password_reset_get(
                request=request,
                url_hash=url_hash,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_password_reset_post(self): #search
        path = f'{self.path}/password_reset_post'

        fixtures = (
            (404, 'not_found',),
            (400, 'invalid',),
            (400, 'required_password1',),
            (200, 'valid',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
            )

            request = response.wsgi_request

            status_code = password_reset_post(
                request=request,
                url_hash=data['url_hash'],
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_get_user(self):
        path = f'{self.path}/get_user'

        fixtures = (
            (200, 'valid',),
            (404, 'not_found',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                username = json.load(file)

            response = self.client.get(path='/')

            request = response.wsgi_request

            status_code, user = get_user(
                request=request,
                username=username,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_profile_post(self):
        path = f'{self.path}/profile_post'
        second_user = CustomUser.objects.create_user(
            email="test2@example.com",
            username="test2",
            password="password123",
            url_hash="ddf7d051-84f6-4a04-a973-f4f57672d8d7",
        )

        fixtures = (
            (200, 'valid',),
            (404, 'not_found',),
            (400, 'required_username',),
            (400, 'unique_username',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            self.client.login(
                email=self.user.email,
                password=self.user.password,
            )

            response = self.client.post(
                path='/',
                data=data,
            )

            request = response.wsgi_request

            status_code = profile_post(
                request=request,
                username=data['current_username'],
            )

            self.assertEqual(status_code, code, msg=fixture)
