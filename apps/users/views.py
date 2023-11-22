from django.shortcuts import render
from rest_framework.decorators import renderer_classes

from rest_framework.viewsets import ModelViewSet

# from config.custom_renderers import CustomRenderer
from .models import *
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.urls.exceptions import Resolver404
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import generics, views

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .serializers import (
    UserMeSerializer,
    DirectorSerializer,
    ManagerSerializer,
    UserSerializer,
    LoginSerializer,
)


class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer
    object = User
    permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ("username", "first_name", "last_name", "role")

    # renderer_classes = [CustomRenderer]

    def get_object(self):
        return self.request.user


class DirectorViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    search_fields = ("username", "first_name", "last_name", "role")

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            director = Director.objects.create_user(
                username=data["username"], password=data["password"]
            )
            serializer = DirectorSerializer(director, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)})

    def update(self, request, *args, **kwargs):
        director = self.get_object()
        data = request.data
        director.username = data.get("username", director.username)
        director.password = data.get("password", director.password)
        director.save()
        serializer = DirectorSerializer(director, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class ManagerViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    search_fields = ("username", "first_name", "last_name", "role")

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            director = Manager.objects.create_user(
                username=data["username"], password=data["password"]
            )
            serializer = ManagerSerializer(director, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except:
            return Response({"error": "Please be aware"})

    def update(self, request, *args, **kwargs):
        director = self.get_object()
        data = request.data
        director.username = data.get("username", director.username)
        director.password = data.get("password", director.password)
        director.save()
        serializer = ManagerSerializer(director, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserViewset(ModelViewSet):
    authentication_classes = [SessionAuthentication]  # Autentifikatsiya turini aniqlash
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ("username", "first_name", "last_name", "role")

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            user = User.objects.create_user(
                username=data["username"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                password=data["password"],
                role=data["role"],
            )
            serializer = UserSerializer(user, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error": "Please be aware"})

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        data = request.data
        user.username = data.get("username", user.username)
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.password = data.get("password", user.password)

        user.save()
        serializer = UserSerializer(user, partial=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:
            refresh = RefreshToken.for_user(user)
            response_data = {
                "user": {
                    "success": True,
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed(
                {
                    "status": False,
                    "message": "Something went wrong during authentication",
                }
            )
