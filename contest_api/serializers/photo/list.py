from rest_framework import serializers

class ListPhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    pub_date = serializers.DateField()

    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    image = serializers.ImageField(source='feed_version')
    num_votes = serializers.IntegerField()
    num_comments = serializers.IntegerField()

