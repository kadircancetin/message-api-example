import factory
from users.factories import UserFactory


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "message.Message"

    sender = factory.SubFactory(UserFactory)
    reciever = factory.SubFactory(UserFactory)
    content = factory.Faker("sentence")
    blocked = False
