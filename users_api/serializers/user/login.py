from rest_framework import serializers

class LoginUserSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()
