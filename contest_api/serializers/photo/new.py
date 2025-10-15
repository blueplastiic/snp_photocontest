from rest_framework import serializers

class NewPhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)

