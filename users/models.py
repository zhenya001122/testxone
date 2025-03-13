from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser, UserManager, PermissionsMixin
from django.db import models


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
    name = models.CharField(max_length=20, default='website',)
    description = models.CharField(max_length=250, blank=True, verbose_name='Краткое описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    user = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        related_name="collections",
        blank=True,
        null=True,)

    def __str__(self):
        return self.name


class Linc(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.CharField(max_length=250, verbose_name='Краткое описание')
    url = models.URLField(unique=True, verbose_name='URL')
    img = models.ImageField(upload_to='img/%Y/%m/%d', default=None,
                              blank=True, null=True, verbose_name='Изображение')
    type = models.ManyToManyField(Collection,
        related_name="URL",)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    user = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        related_name="URL",
        blank=True,
        null=True, )

