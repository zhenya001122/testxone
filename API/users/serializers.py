from django.contrib.auth import get_user_model
from django.template.defaultfilters import title
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from parser.parser import parsing
from users.models import Collection, CustomUser, Linc
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()

class CollectionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset = CustomUser.objects,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Collection
        fields = ('name', 'description', 'user')


class LincSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='email',
        queryset=CustomUser.objects,
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Linc
        fields = ('url', 'user', 'type', 'title', 'description', 'image', 'image_file')


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'password')


class CustomUserSerializer(UserSerializer):
    collections = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta(UserSerializer.Meta):
        model = User
        fields = ('email', 'collections')

