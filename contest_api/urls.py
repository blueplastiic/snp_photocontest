from django.urls import path
from contest_api.views.photo.create import CreatePhotoAPIView
from contest_api.views.photo.detail import PhotoDetailAPIView
from contest_api.views.vote.views import VoteAPIView

app_name = 'contest_api'

urlpatterns=[ 
    path('photo/<int:id>/', PhotoDetailAPIView.as_view(), name='photo_detail'),
    path('photo/create/', CreatePhotoAPIView.as_view(), name='photo_create'),
    path('photo/<int:id>/vote', VoteAPIView.as_view(), name='vote'),
]

