from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, extend_schema_view
from API.users.serializers import CollectionSerializer, LincSerializer
from parser.parser import parsing
from users.models import Collection, Linc, CustomUser


class LincAPIList(generics.ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = LincSerializer
    permission_classes = (IsAuthenticated,)
    @extend_schema(
        summary="Добавление ссылки",
        description="Добавляет ссылку пользователя. Ссылка не может повторяться",
        request=LincSerializer,
        responses={
            201: OpenApiResponse(response=LincSerializer, description="Ссылка успешно добавлена"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def create(self, request, *args, **kwargs):
        queryset = Linc.objects.filter(user_id=request.user.id)
        parser_dict = parsing(request.data["url"])
        print(parser_dict)
        for i in queryset:
            if request.data['url'] == i.url:
                return Response({'linc': f'ссылка {request.data['url']} уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data={**request.data.dict(), **parser_dict})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LincAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Linc.objects.all()
    serializer_class = LincSerializer
    permission_classes = (IsAuthenticated,)


@extend_schema_view(
    get=extend_schema(
        summary="Получение информации о коллекциях пользователя",
        description="Возвращает список всех коллекций пользователя.",
        responses={
            200: OpenApiResponse(response=CollectionSerializer(many=True), description="Список коллекций пользователея")
        }
    ),
    post=extend_schema(
        summary="Добавление коллекции пользователя",
        description="Добавляет коллекцию пользователя пользователя. Коллекция не может повторяться",
        request=CollectionSerializer,
        responses={
            201: OpenApiResponse(response=CollectionSerializer, description="Коллекция успешно добавлена"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    ),
)
class CollectionAPIList(generics. ListCreateAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        pk = request.user.id
        queryset = Collection.objects.filter(user_id=pk)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        queryset = Collection.objects.filter(user_id=request.user.id)
        for i in queryset:
            if request.data['name'] == i.name:
                return Response({'collection': f'коллекция {request.data['name']} уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema_view(
    get=extend_schema(
        summary="Получение информации о коллекции пользователя",
        description="Возвращает коллекцию пользователя.",
        responses={
            200: OpenApiResponse(response=CollectionSerializer, description="Коллекция пользователея")
        }
    ),
    put=extend_schema(
        summary="Изменение коллекции пользователя",
        description="Заменяет все поля объекта данными запроса.",
        request=CollectionSerializer,
        responses={
            200: OpenApiResponse(response=CollectionSerializer, description="Коллекция успешно изменена"),
        }
    ),
    patch=extend_schema(
        summary="Частичное изменение коллекции пользователя",
        description="Частично заменяет поля объекта данными запроса.",
        request=CollectionSerializer,
        responses={
            200: OpenApiResponse(response=CollectionSerializer, description="Коллекция успешно изменена"),
        }
    ),
    delete=extend_schema(
        summary="Удаление коллекции пользователя",
        description="Удаляет коллекцию пользователя.",
        responses={
            204: OpenApiResponse(description="Коллекция успешно удалена"),
        }
    ),
)
class CollectionAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = (IsAuthenticated,)
