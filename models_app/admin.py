from django.contrib import admin
from .models.user.models import User 
from .models.photo.models import Photo
from .models.vote.models import Vote
from .models.comment.models import Comment


admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Vote)
admin.site.register(Comment)

