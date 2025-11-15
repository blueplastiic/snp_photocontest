from rest_framework import serializers

class RetrievePhotoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    pub_date = serializers.DateField()

    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    image = serializers.ImageField()

    num_votes = serializers.IntegerField()

