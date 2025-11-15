from rest_framework import serializers

class RetrieveTokenSerializer(serializers.Serializer):
    auth_token = serializers.CharField()
