from rest_framework import serializers
from .models import User



class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=30)
    about = serializers.CharField(max_length=500, required=False)

class UserPrivateGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    about = serializers.CharField(max_length=500)

class UserPublicGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=20)
    about = serializers.CharField(max_length=500)

