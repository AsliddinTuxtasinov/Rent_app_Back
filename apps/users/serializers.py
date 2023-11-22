from rest_framework import serializers, exceptions, status
from .models import *
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'username', 'role']
        fields = ("id", "username", "password", "first_name", "last_name", "role")


#
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        # fields = ['id', 'username', 'role']
        fields = ("id", "username", "first_name", "last_name", "role")


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        # fields = ['id', 'username', 'role']
        fields = ("id", "username", "first_name", "last_name", "role")


# class LoginSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(max_length=223, required=True)
#     password = serializers.CharField(max_length=68, write_only=True)
#     first_name = serializers.CharField(max_length=223, read_only=True)
#     last_name = serializers.CharField(max_length=223, read_only=True)
#
#     # role = serializers.ChoiceField(max_length=223, read_only=True)
#     def get_fist_name(self, obj):
#         username = obj.get("username")
#         user = User.objects.filter(username=username).first()
#         return user.first_name
#
#     def get_last_name(self, obj):
#         username = obj.get("username")
#         user = User.objects.filter(username=username).first()
#         return user.last_name
#
#     def role(self, obj):
#         role = obj.get("role")
#         user = User.objects.filter(role=role).first()
#         return user.role
#
#     class Meta:
#         model = User
#         fields = ("id", "username", "first_name", "last_name", "role", "password")
#
#     def validate(self, attrs):
#         username = attrs.get("username")
#         password = attrs.get("password")
#         role = attrs.get("role")
#         user = authenticate(username=username, password=password, role=role)
#         if not user:
#             raise AuthenticationFailed(
#                 {"status": False, "message": "Username or password is not correct"}
#             )
#
#         data = {
#             "success": True,
#             "id": user.id,
#             "username": user.username,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "role": user.role,
#         }
#         refresh = RefreshToken.for_user(user)
#         data["refresh"] = str(refresh)
#         data["access"] = str(refresh.access_token)
#
#         return data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=223, required=True)
    password = serializers.CharField(max_length=68, required=True)

    # def validate(self, attrs):
    #     username = attrs.get("username")
    #     password = attrs.get("password")
    #     user = authenticate(username=username, password=password)
    #
    #     if not user:
    #         raise serializers.ValidationError(
    #             {"status": False, "message": "Username or password is not correct"},
    #             code="authentication"
    #         )
    #
    #     data = {
    #         "success": True,
    #         "id": user.id,
    #         "username": user.username,
    #         "first_name": user.first_name,
    #         "last_name": user.last_name,
    #         "role": user.role,
    #     }
    #     refresh = RefreshToken.for_user(user)
    #     data["refresh"] = str(refresh)
    #     data["access"] = str(refresh.access_token)
    #     print(data)
    #     return data

    @staticmethod
    def validate_username(username):
        # Check if the username length is between 5 and 30 characters
        if len(username) < 4 or len(username) > 30:
            raise exceptions.ValidationError(
                {"message": "username must be between 4 and 30 characters"},
                status.HTTP_400_BAD_REQUEST,
            )

        # Check if the username contains only digits
        # elif username.isdigit():
        #     raise exceptions.ValidationError({
        #         "message": "username should not consist of alpha numerics"
        #     }, status.HTTP_400_BAD_REQUEST)

        return username
