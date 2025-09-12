from rest_framework import serializers

class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20)
    about = serializers.CharField(max_length=500)

