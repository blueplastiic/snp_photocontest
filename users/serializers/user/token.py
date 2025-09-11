from rest_framework import serializers

class UserTokenSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    token = serializers.CharField()

