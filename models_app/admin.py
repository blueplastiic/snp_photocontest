from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Photo)
admin.site.register(Vote)
admin.site.register(Comment)

