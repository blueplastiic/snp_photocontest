from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    auth_token = serializers.CharField()

