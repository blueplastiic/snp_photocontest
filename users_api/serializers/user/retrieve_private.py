from rest_framework import serializers

class UserPrivateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=20)
    about = serializers.CharField(max_length=500)

