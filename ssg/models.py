from django.db import models
from django.utils import timezone


class User(models.Model):
    user_id = models.CharField(max_length=30, unique=True)
    user_password = models.CharField(max_length=30)
    user_email = models.CharField(max_length=30)
    user_avatar = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="./")
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)