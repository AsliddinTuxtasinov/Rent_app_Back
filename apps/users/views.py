from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from apps.users.serializers import *
from .models import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.urls.exceptions import Resolver404
from rest_framework import generics, status
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

# Director Table
class DirectorViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset =  Director.objects.all()
    serializer_class = DirectorSerializer
    def create(self, request, *args, **kwargs):
        data =  request.data
        try:
            director = Director.objects.create_user(username=data['username'],password=data['password'])
            serializer = DirectorSerializer(director,partial=True)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        except:
            return Response({'error':'Please be aware'})
    def update(self, request, *args, **kwargs):
        director  =  self.get_object()
        data = request.data
        director.username = data.get('username',director.username)
        director.password = data.get('password',director.password)
        director.save()
        serializer = DirectorSerializer(director,partial=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
class UserViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset =  User.objects.all()
    serializer_class =UserSerializer
    def create(self, request, *args, **kwargs):
        data =  request.data
        try:
            user = User.objects.create_user(username=data['username'],password=data['password'])
            serializer =UserSerializer(user,partial=True)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({'error':'Please be aware'})
    def update(self, request, *args, **kwargs):
        user  =  self.get_object()
        data = request.data
        user.username = data.get('username',user.username)
        user.password = data.get('password',user.password)
        user.save()
        serializer = UserSerializer(user,partial=True)
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    
class LoginAPIView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = []
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)