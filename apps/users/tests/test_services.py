import json
import os

from django.test import (
    TestCase,
    Client,
)

from users.models import CustomUser
from users.services import (
    create_and_return_user,
    is_user_logged_in,
    register_user,
    login_user,
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
        )
        # cls.client = Client()
        # cls.response = cls.client.get('/')
        # cls.request = cls.response.wsgi_request

    def test_create_and_return_user(self):
        response = self.client.get('/')
        request = response.wsgi_request

        fixtures = (
            (200, 'valid',),
            (500, 'invalid_1',),
            (500, 'invalid_2',),
        )

        for status in fixtures:
            with open(f'{self.path}/create_and_return_user_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            code, user = create_and_return_user(
                request=request,
                data=data,
            )

            self.assertEqual(code, status[0], msg=status)

    def test_is_user_logged_in(self):
        response = self.client.get('/')
        request = response.wsgi_request

        fixtures = (
            (200, 'valid',),
            (401, 'invalid_1',),
        )

        for status in fixtures:
            with open(f'{self.path}/is_user_logged_in_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            code = is_user_logged_in(
                request=request,
                data=data,
            )

            self.assertEqual(code, status[0], msg=status)

    def test_register_user(self):
        fixtures = (
            (200, 'valid',),
            (400, 'invalid_1',),
            (400, 'invalid_2',),
            (400, 'invalid_3',),
        )

        for status in fixtures:
            with open(f'{self.path}/register_user_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
            )
            request = response.wsgi_request

            code = register_user(
                request=request,
            )

            self.assertEqual(code, status[0], msg=status)

    def test_login_user(self):
        fixtures = (
            (200, 'valid',),
            (400, 'invalid_1',),
            (400, 'invalid_2',),
            (401, 'invalid_1',),
        )

        for status in fixtures:
            with open(f'{self.path}/login_user_{status[0]}_{status[1]}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
            )
            request = response.wsgi_request

            code = login_user(
                request=request,
            )

            self.assertEqual(code, status[0], msg=status)
