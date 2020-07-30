from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.CharField(max_length=30)
    user_password = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_avatar = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user_id


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    picture = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
