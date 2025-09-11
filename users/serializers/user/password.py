from rest_framework import serializers

class UserConfirmActionSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=30)

