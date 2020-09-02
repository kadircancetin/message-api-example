from core.tests import BaseViewTestCase
from rest_framework import status
from users.factories import BlockFactory

from message.factories import MessageFactory
from message.models import Message


class MessageCreateViewTestCase(BaseViewTestCase):
    def setUp(self):
        self.path = "/message/{}/"
        self.anonymous_client = self.get_anonymous_client()

        self.user1, self.user1_client = self.create_user_and_get_client()
        self.user2, self.user2_client = self.create_user_and_get_client()
        self.user1_path = self.path.format(self.user1.id)
        self.user2_path = self.path.format(self.user2.id)

        self.example_content = "naber"
        self.example_data = {
            "content": self.example_content,
        }

    def test_permissions(self):
        response = self.anonymous_client.get(self.user1_path)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.anonymous_client.post(self.user1_path, data=self.example_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.user1_client.get(self.user1_path)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)
        response = self.user1_client.post(self.user1_path, data=self.example_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

    def test_post_new_message(self):
        response = self.user1_client.post(self.user2_path, data=self.example_data)
        message = Message.objects.get(id=response.data["id"])
        self.assertEqual(message.content, self.example_content)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.reciever, self.user2)
        self.assertEqual(message.blocked, False)

    def test_post_new_message_to_blocked_user(self):
        BlockFactory(blocker=self.user2, blocked=self.user1)

        response = self.user1_client.post(self.user2_path, data=self.example_data)
        message = Message.objects.get(id=response.data["id"])
        self.assertEqual(message.content, self.example_content)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.reciever, self.user2)
        self.assertEqual(message.blocked, True)

    def test_get_meesages(self):
        self.assertFalse(
            Message.objects.filter(sender=self.user1, reciever=self.user2).exists()
        )

        messages_1to2 = MessageFactory.create_batch(
            3, sender=self.user1, reciever=self.user2
        )
        messages_2to1 = MessageFactory.create_batch(
            5, sender=self.user1, reciever=self.user2
        )
        messages_1to2_2 = MessageFactory.create_batch(
            2, sender=self.user1, reciever=self.user2
        )

        response_user2 = self.user2_client.get(self.user1_path, data=self.example_data)
        response_user1 = self.user1_client.get(self.user2_path, data=self.example_data)
        self.assertEqual(response_user1.data["results"], response_user2.data["results"])
        self.assertEqual(response_user1.data["count"], 10)

        result_ids = [x["id"] for x in response_user1.data["results"]]
        expected_ids = [x.id for x in messages_1to2 + messages_2to1 + messages_1to2_2]
        expected_ids.reverse()
        self.assertEqual(expected_ids, result_ids)

    def test_blocked_user_meesages(self):
        self.assertFalse(
            Message.objects.filter(sender=self.user1, reciever=self.user2).exists()
        )

        messages_not_blocked = MessageFactory(
            sender=self.user1, reciever=self.user2, blocked=False
        )
        MessageFactory(sender=self.user1, reciever=self.user2, blocked=True)

        response = self.user1_client.get(self.user2_path, data=self.example_data)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], messages_not_blocked.id)
