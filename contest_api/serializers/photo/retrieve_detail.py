from rest_framework import serializers

class PhotoDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    pub_date = serializers.DateField()
    photo = serializers.ImageField()
    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')
    num_votes = serializers.IntegerField()

