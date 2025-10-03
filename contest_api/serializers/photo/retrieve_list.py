from rest_framework import serializers

class PhotoListSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300)
    pub_date = serializers.DateField()

    user_id = serializers.IntegerField(source='user.id')
    username = serializers.CharField(source='user.username')

    photo = serializers.ImageField(source='feed_version')
    num_votes = serializers.IntegerField()
    num_comments = serializers.IntegerField()

    status = serializers.CharField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if self.context['user'] != instance.user: #pyright: ignore
            ret.pop('status')
        return ret

