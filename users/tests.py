from core.tests import BaseViewTestCase
from rest_framework import status
from rest_framework.authtoken.models import Token

from users.factories import BlockFactory, UserFactory
from users.models import Block


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


class UserLoginTestCase(BaseViewTestCase):
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

        token = Token.objects.get(key=response.data["token"])
        self.assertEqual(token.user, self.user)

    def test_unsuccessfully_login(self):
        self.example_data["password"] = "wrongpassword"
        response = self.anonymous_client.post(self.path, self.example_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class BlockUserViewTestCase(BaseViewTestCase):
    def setUp(self):
        self.path = "/user/block/{}/"
        self.anonymous_client = self.get_anonymous_client()
        self.user1, self.user1_client = self.create_user_and_get_client()
        self.user2, self.user2_client = self.create_user_and_get_client()
        self.block_user2_path = self.path.format(self.user2.id)

    def test_permissions(self):
        response = self.anonymous_client.post(self.block_user2_path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.user1_client.post(self.block_user2_path)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_404_on_worng_user_block(self):
        response = self.user1_client.post("1231231231312312313")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_block(self):
        self.assertFalse(
            Block.objects.filter(blocker=self.user1, blocked=self.user2).exists()
        )

        response = self.user1_client.post(self.block_user2_path)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            Block.objects.filter(blocker=self.user1, blocked=self.user2).exists()
        )

    def test_multi_block_request(self):
        self.assertFalse(
            Block.objects.filter(blocker=self.user1, blocked=self.user2).exists()
        )

        response = self.user1_client.post(self.block_user2_path)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.user1_client.post(self.block_user2_path)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            Block.objects.filter(blocker=self.user1, blocked=self.user2).count(), 1
        )


class UnBlockUserView(BaseViewTestCase):
    def setUp(self):
        self.path = "/user/unblock/{}/"
        self.anonymous_client = self.get_anonymous_client()
        self.blocker, self.blocker_client = self.create_user_and_get_client()
        self.blocked, self.blocked_client = self.create_user_and_get_client()
        self.unblock_path = self.path.format(self.blocked.id)

        BlockFactory(blocker=self.blocker, blocked=self.blocked)

    def test_permissions(self):
        response = self.anonymous_client.post(self.unblock_path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.blocker_client.post(self.unblock_path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_404_on_worng_user_unblock(self):
        response = self.blocker_client.post("1231231231312312313")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unblock(self):
        self.assertTrue(
            Block.objects.filter(blocker=self.blocker, blocked=self.blocked).exists()
        )

        response = self.blocker_client.post(self.unblock_path)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Block.objects.filter(blocker=self.blocker, blocked=self.blocked).exists()
        )
