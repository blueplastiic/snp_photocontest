from django.conf import settings
from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from utils.statuses import PhotoStatus


class Photo(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    pub_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1,choices=PhotoStatus.STATUS_CHOICES, default=PhotoStatus.PENDING)

    original_version = models.ImageField(upload_to='photos')

    feed_version = ImageSpecField(
        source='original_version', 
        format='JPEG', 
        processors=[ResizeToFit(600,400)],
        options={'quality':75}
                                  )
    thumbnail_version = ImageSpecField(
        source='original_version',
        format='JPEG',
        processors=[ResizeToFit(100,100)],
        options={'quality': 50}
    )
    class Meta:
        permissions = [('change_status', 'Can change the status of tasks')]


class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'photo'], name='unique_vote')
        ]

class Comment(models.Model):
    content = models.TextField(max_length=500)
    publish_date = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)


