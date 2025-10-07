from django.urls import path
from contest_api.views.photo.create import CreatePhotoAPIView
from contest_api.views.photo.detail import PhotoDetailAPIView

from contest_api.views.vote.create import CreateVoteAPIView
from contest_api.views.vote.delete import DeleteVoteAPIView

app_name = 'contest_api'

urlpatterns=[ 
    path('photo/<int:id>/', PhotoDetailAPIView.as_view(), name='photo_detail'),
    path('photo/create/', CreatePhotoAPIView.as_view(), name='photo_create'),

    path('vote/', CreateVoteAPIView.as_view(), name='vote_create'),
    path('vote/<int:vote_id>/', DeleteVoteAPIView.as_view(), name='vote_delete') #but how do we actually get the vote id?
]

