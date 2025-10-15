from rest_framework import serializers
from .children import ChildrenCommentSerializer

class ParentCommentSerializer(serializers.Serializer):
    content = serializers.TimeField()
    publish_date=serializers.DateTimeField()

    username=serializers.CharField(source='user.username')
    user_id=serializers.IntegerField(source='user.id')

    chilrden = ChildrenCommentSerializer(many=True, source='children')

