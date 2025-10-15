from rest_framework import serializers

class ChildrenCommentSerializer(serializers.Serializer):
    content = serializers.TimeField()
    publish_date=serializers.DateTimeField()

    username=serializers.CharField(source='user.username')
    user_id=serializers.IntegerField(source='user.id')

