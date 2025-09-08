from rest_framework import serializers

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=30)
    about = serializers.CharField(max_length=500, required=False)
    avatar = serializers.ImageField(required=False)

class UserGetTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    token = serializers.CharField()

class UserPrivateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    about = serializers.CharField(max_length=500)

class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    about = serializers.CharField(max_length=500)
    avatar = serializers.ImageField(required=False)

class UserConfirmActionSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)

