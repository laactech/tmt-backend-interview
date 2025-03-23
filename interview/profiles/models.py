from django.contrib.auth.models import AbstractUser
from django.db import models



class UserProfile(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    date_joined = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="avatars/%Y/%m/%d/")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_username(self):
        return self.email

    @property
    def is_authenticated(self):
        return True