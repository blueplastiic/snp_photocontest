from django.db import models
from django.conf import settings

class Comment(models.Model):
    content = models.TextField(max_length=500)
    publish_date = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', related_name = 'comments', on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey('self', related_name = 'children', on_delete=models.CASCADE, null=True)

