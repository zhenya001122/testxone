from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.core.files.base import ContentFile
from django.db import models
from django.core.files import File
from urllib import request
import os
import requests


class NewUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,)
        user.set_password(password)
        user.save(using=self.db)

        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = NewUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email


class Collection(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=250, blank=True, verbose_name='Краткое описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    linc = models.ManyToManyField("Linc",
        related_name="URL",)
    user = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        related_name="collections",
        blank=True,
        null=True,)

    def __str__(self):
        return self.name


class Linc(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.CharField(max_length=250, blank=True, null=True, verbose_name='Краткое описание')
    url = models.URLField(verbose_name='URL')
    image_file = models.ImageField(upload_to='images', default=None, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=100, default='website')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    user = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        related_name="URL",
        blank=True,
        null=True, )

    def save(self, *args, **kwargs):
        if self.image and not self.image_file:
            p = requests.get(self.image)
            filename = self.image.rsplit('/', 1)[1]
            self.image_file.save(
                filename,
                ContentFile(p.content)
            )
            super(Linc, self).save()
        super(Linc, self).save()

    def __str__(self):
        return self.url
