from rest_framework import serializers

class PhotoDetailSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    pub_date = serializers.DateField()
    photo = serializers.ImageField()
    user_id = serializers.IntegerField()
    num_votes = serializers.IntegerField()

