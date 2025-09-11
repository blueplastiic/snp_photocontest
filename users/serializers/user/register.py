from rest_framework import serializers

class UserRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=30)
    about = serializers.CharField(max_length=500, required=False)

