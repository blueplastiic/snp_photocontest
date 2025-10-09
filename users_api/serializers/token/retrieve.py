from rest_framework import serializers

class RetrieveTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    auth_token = serializers.CharField()

