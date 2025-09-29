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

    photo = models.ImageField(upload_to='photos')

    feed_version = ImageSpecField(
        source='photo', 
        format='JPEG', 
        processors=[ResizeToFit(600,400)],
        options={'quality':75}
                                  )
    thumbnail_version = ImageSpecField(
        source='photo',
        format='JPEG',
        processors=[ResizeToFit(100,100)],
        options={'quality': 50}
    )
    class Meta:
        permissions = [('change_status', 'Can change the status of tasks')]

