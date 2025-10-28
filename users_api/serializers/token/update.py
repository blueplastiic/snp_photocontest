from rest_framework import serializers

class UpdateTokenSerializer(serializers.Serializer):
    key = serializers.CharField()
