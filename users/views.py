from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from API.users.serializers import UserSerializer, CollectionSerializer
from users.models import Collection, CustomUser


class UserRegistration(APIView):
    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным email",
        request=UserSerializer,
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации")
        }
    )

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'user': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Метод PUT не разрешен"})

        try:
            instance = CustomUser.objects.get(pk=pk)
        except:
            return Response({"error": "Пользователь не существует"})

        serializer = UserSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"user": serializer.data})


class UserDelete(APIView):
    @extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя по его ID. Если пользователь не найден, возвращает ошибку.",
        responses={
            200: OpenApiResponse(description="Пользователь успешно удалён"),
            404: OpenApiResponse(description="Пользователь не найден"),
            400: OpenApiResponse(description="ID пользователя не предоставлен")
        }
    )
    def delete(self, request, pk):
        if pk:
            try:
                user = CustomUser.objects.get(id=pk)
                user.delete()
                return Response({"status": "User deleted"}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user = authenticate(
            request, username=request.data["email"], password=request.data["password"]
        )
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        token = Token.objects.get_or_create(user=user)[0].key
        return Response(status=status.HTTP_200_OK, data={"token": token})


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