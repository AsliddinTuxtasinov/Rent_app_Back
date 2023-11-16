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



class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer
    object = User
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


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
    
    
# Manager Table
class ManagerViewset(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset =  Manager.objects.all()
    serializer_class = ManagerSerializer
    def create(self, request, *args, **kwargs):
        data =  request.data
        try:
            manager = Manager.objects.create_user(username=data['username'],password=data['password'])
            serializer = ManagerSerializer(manager,partial=True)
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        except:
            return Response({'error':'Please be aware'})
    def update(self, request, *args, **kwargs):
        manager  =  self.get_object()
        data = request.data
        manager.username = data.get('username',manager.username)
        manager.password = data.get('password',manager.password)
        manager.save()
        serializer = ManagerSerializer(manager,partial=True)
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


# class UserMeViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['post'], url_path='me')
#     def get_my_data(self, request):
#         serializer = MeSerializer(data={'token': request.auth})
#         if serializer.is_valid():
#             user_data = serializer.validated_data
#             return Response(user_data)
#         else:
#             raise AuthenticationFailed("Invalid token")