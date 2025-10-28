from rest_framework import serializers

class NewCommentSerializer(serializers.Serializer):
    content = serializers.CharField()
    photo_id = serializers.IntegerField() 

