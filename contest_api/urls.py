from django.urls import path
from contest_api.views.photo import detail
from contest_api.views.photo import create

app_name = 'contest_api'

urlpatterns=[
     path('photo/<int:id>/', detail.PhotoDetailAPIView.as_view(), name='photo_create'),
     path('photo/create/', create.CreatePhotoAPIView.as_view(), name='photo_detail'),
]

