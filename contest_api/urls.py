from django.urls import path

from contest_api.views.vote.views import CreateVoteAPIView, DeleteVoteAPIView
from contest_api.views.comment.views import ListCreateCommentAPIView, UpdateDeleteCommentAPIView
from contest_api.views.photo.views import ListCreatePhotoAPIView, ListCurrentUserPhotoAPIView, ListUserPhotoAPIView, RetrieveUpdateDeletePhotoAPIView


urlpatterns=[ 
    path('photos/', ListCreatePhotoAPIView.as_view()),
    path('photos/<int:photo_id>/', RetrieveUpdateDeletePhotoAPIView.as_view()),

    path('photos/user/<int:user_id>/', ListUserPhotoAPIView.as_view()),
    path('photos/me/', ListCurrentUserPhotoAPIView.as_view()),

    path('vote/', CreateVoteAPIView.as_view(), name='vote_create'),
    path('vote/<int:photo_id>/', DeleteVoteAPIView.as_view(), name='vote_delete'),

    path('photos/<int:photo_id>/comments/', ListCreateCommentAPIView.as_view()),
    path('comments/<int:comment_id>', UpdateDeleteCommentAPIView.as_view()),
]

