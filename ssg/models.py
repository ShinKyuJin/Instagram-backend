from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    def create_user(self, email, password, is_admin=False, **kwargs):
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, is_admin=True, **kwargs):
        return self._create_user(email, password, **kwargs)

    def get_by_natural_key(self, email):
        return self.get(email=email)


class User(AbstractBaseUser, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    username = models.CharField(max_length=30)
    avatar = models.ImageField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="/")
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

