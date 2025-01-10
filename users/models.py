from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.email}'  # Строковое представление объекта


class Collection(models.Model):
    name = models.CharField(max_length=20, verbose_name='коллекция')
    description = models.CharField(max_length=250, blank=True, verbose_name='Краткое описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    user = models.ForeignKey(CustomUser,
        on_delete=models.CASCADE,
        related_name="collections",
        blank=True,
        null=True,)

    def __str__(self):
        return f'{self.name}'


class Linc(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    description = models.CharField(max_length=250, verbose_name='Краткое описание')
    url = models.URLField(unique=True, verbose_name='URL')
    img = models.ImageField(upload_to='img/%Y/%m/%d', default=None,
                              blank=True, null=True, verbose_name='Изображение')
    type = models.ManyToManyField(Collection)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    user = models.ForeignKey(CustomUser,
         on_delete=models.CASCADE,
         related_name="URL",
         blank=True,
         null=True, )

