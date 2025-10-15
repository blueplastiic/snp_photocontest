from rest_framework import serializers

class NewCommentSerializer(serializers.Serializer):
    content = serializers.TimeField()
    photo_id = serializers.IntegerField() 

