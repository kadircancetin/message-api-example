from core.tests import BaseViewTestCase
from rest_framework import status
from users.factories import UserFactory
from rest_framework.authtoken.models import Token


class UserCreateViewTestCase(BaseViewTestCase):
    def setUp(self):
        self.path = "/user/register/"
        self.anonymous_client = self.get_anonymous_client()

        self.example_data = {
            "username": "kadir",
            "password": "kadir123456",
        }

    def test_create_user(self):
        response = self.anonymous_client.post(self.path, self.example_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cant_create_multiple_user(self):
        response = self.anonymous_client.post(self.path, self.example_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.anonymous_client.post(self.path, self.example_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginCase(BaseViewTestCase):
    def setUp(self):
        self.path = "/user/login/"
        self.anonymous_client = self.get_anonymous_client()

        self.password = "testpassword"
        self.user = UserFactory(password=self.password)
        self.example_data = {
            "username": self.user.username,
            "password": self.password,
        }

    def test_successfully_login(self):
        response = self.anonymous_client.post(self.path, self.example_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = Token.objects.get(key=response.data['token'])
        self.assertEqual(token.user, self.user)

    def test_unsuccessfully_login(self):
        self.example_data['password'] = "wrongpassword"
        response = self.anonymous_client.post(self.path, self.example_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
