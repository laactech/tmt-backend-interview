from django.test import TestCase
from interview.profiles.models import UserProfile


class TestUserProfile(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )

    def test_get_full_name(self):
        self.assertEqual(self.user.get_full_name(), "John Doe")

    def test_get_full_name_empty_first(self):
        self.user.first_name = ""
        self.user.save()
        self.assertEqual(self.user.get_full_name(), " Doe")

    def test_get_full_name_empty_last(self):
        self.user.first_name = "John"
        self.user.last_name = ""
        self.user.save()
        self.assertEqual(self.user.get_full_name(), "John ")

    def test_get_full_name_empty(self):
        self.user.first_name = ""
        self.user.last_name = ""
        self.user.save()
        self.assertEqual(self.user.get_full_name(), " ")

    def test_get_username(self):
        self.assertEqual(self.user.get_username(), "test@example.com")

        self.user.email = "newemail@example.com"
        self.user.save()
        self.assertEqual(self.user.get_username(), "newemail@example.com")
