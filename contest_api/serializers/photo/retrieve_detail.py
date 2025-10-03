from rest_framework import serializers

class PhotoDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    pub_date = serializers.DateField()

    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    photo = serializers.ImageField(source='photo')
    num_votes = serializers.IntegerField()
    #comments

