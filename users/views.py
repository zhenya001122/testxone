from django.contrib.auth import authenticate
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, extend_schema_view
from API.users.serializers import CollectionSerializer
from users.models import Collection, CustomUser


class CollectionCreate(APIView):
    @extend_schema(
        summary="Добавление коллекци",
        description="Добавляет коллекцию пользователя. Коллекция не может повторяться",
        request=CollectionSerializer,
        responses={
            201: OpenApiResponse(response=CollectionSerializer, description="Коллекция успешно добавлена"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )
    def post(self, request):
        collections = Collection.objects.filter(user_id=request.data['user'])
        for i in collections:
            if request.data['name'] == i.name:
                return Response({'collection': f'коллекция {request.data['name']} уже существует'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CollectionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            collection = serializer.save()
            return Response({"status": f"коллекция {collection} успешно добавлена"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CollectionList(APIView):
    @extend_schema(
        summary="Получение информации о коллекциях пользователя",
        description="Возвращает список всех коллекций пользователя.",
        responses={
            200: OpenApiResponse(response=CollectionSerializer(many=True), description="Список коллекций пользователея")
        }
    )
    def get(self, request):
        pk = request.data['user']
        if not pk:
            return Response({"error": "Method GET not allowed"})

        try:
            collections = Collection.objects.filter(user_id=pk)
        except:
            return Response({"error": "Collection not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = CollectionSerializer(collections, many=True)
        return Response(serializer.data)

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