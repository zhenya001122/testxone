from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import CustomUser, Collection
from djoser.serializers import UserCreateSerializer

User = get_user_model()

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        exclude = ['time_create', 'time_update',]


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'password', )