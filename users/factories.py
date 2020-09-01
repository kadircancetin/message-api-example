import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
        django_get_or_create = ("username",)

    username = factory.LazyAttributeSequence(lambda o, n: "user_{}".format(n))
    first_name = factory.LazyAttribute(lambda obj: f"{obj.username}_first_name")
    last_name = factory.LazyAttribute(lambda obj: f"{obj.username}_last_name")
    email = factory.LazyAttribute(
        lambda obj: f'{obj.username}@{factory.Faker("free_email_domain").generate()}'
    )
    password = factory.PostGenerationMethodCall(
        "set_password", factory.Faker("password").generate()
    )
    is_staff = False
