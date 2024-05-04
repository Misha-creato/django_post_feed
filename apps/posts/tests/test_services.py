import json
import os

from django.test import (
    TestCase,
)

from posts.models import Post
from posts.services import update_or_create_post, get_post, search_posts, hide_post
from users.models import CustomUser


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

        cls.post = Post.objects.create(
            user=cls.user,
            title="Test title",
            description="Test description",
        )

    def test_get_post(self):
        path = f'{self.path}/get_post'

        self.client.login(
            email="test1@example.com",
            password="password123",
        )

        response = self.client.get(path='/')
        request = response.wsgi_request

        fixtures = (
            (404, 'not_found',),
            (200, 'valid',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            status_code, post = get_post(
                request=request,
                slug=data.get('slug', self.post.slug),
                detail=data['detail'],
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_update_or_create_post(self):
        path = f'{self.path}/update_or_create_post'

        fixtures = (
            (200, 'valid_create',),
            (200, 'valid_update',),
            (400, 'invalid',),
            (400, 'required_title',),
        )

        self.client.login(
            email="test1@example.com",
            password="password123",
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            response = self.client.post(
                path='/',
                data=data,
                format='json',
            )

            request = response.wsgi_request

            status_code, post = update_or_create_post(
                request=request,
                action=data['action'],
                slug=data.get('slug', self.post.slug),
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_search_post(self):
        path = f'{self.path}/search_posts'

        fixtures = (
            (200, 'valid',),
            (404, 'not_found',),
        )

        self.client.login(
            email="test1@example.com",
            password="password123",
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            response = self.client.get(
                path='/',
                data=data,
            )

            request = response.wsgi_request

            status_code, posts = search_posts(
                request=request,
            )

            self.assertEqual(status_code, code, msg=fixture)

    def test_hide_post(self):
        second_user = CustomUser.objects.create_user(
            email="test2@example.com",
            username="test2",
            password="password123",
            url_hash="ddf7d051-84f6-4a04-a973-f4f57672d8d7",
        )

        path = f'{self.path}/hide_post'

        fixtures = (
            (200, 'valid',),
            (403, 'forbidden',),
            (404, 'not_found',),
        )

        for code, name in fixtures:
            fixture = f'{code}_{name}'
            with open(f'{path}/{fixture}_request.json') as file:
                data = json.load(file)

            self.client.login(
                email=data['email'],
                password=data['password'],
            )

            response = self.client.get(path='/')

            request = response.wsgi_request

            status_code = hide_post(
                request=request,
                slug=data.get('slug', self.post.slug)
            )

            self.assertEqual(status_code, code, msg=fixture)
