from rest_framework import serializers
from users.models import CustomUser, Collection


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password',]


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        exclude = ['time_create', 'time_update',]
