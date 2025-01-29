from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from API.users.serializers import UserSerializer, CollectionSerializer
from users.models import Collection, CustomUser


class CollectionCreate(APIView):
    def post(self, request):
        collections = Collection.objects.filter(user_id=request.data['user'])
        for i in collections:
            if request.data['name'] == i.name:
                return Response({'collection': f'коллекция существует'})
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'collection': serializer.data})