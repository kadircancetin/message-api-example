from django.test import TestCase
from rest_framework.test import APIClient
from users.factories import UserFactory


class BaseViewTestCase(TestCase):
    @classmethod
    def get_anonymous_client(cls):
        return APIClient()

    @classmethod
    def create_user_and_get_client(cls, **user_data):
        user = UserFactory(**user_data)
        client = APIClient()
        client.force_authenticate(user=user)
        return user, client
