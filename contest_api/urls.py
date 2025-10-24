from django.urls import path

from contest_api.views.vote.views import CreateVoteAPIView, DeleteVoteAPIView
from contest_api.views.comment.views import ListCreateCommentAPIView, UpdateDeleteCommentAPIView
from contest_api.views.photo.views import ListCreatePhotoAPIView, ListCurrentUserPhotoAPIView, ListUserPhotoAPIView, RetrieveUpdateDeletePhotoAPIView


urlpatterns=[ 

    path('vote/', CreateVoteAPIView.as_view()),
    path('vote/<int:photo_id>/', DeleteVoteAPIView.as_view()),

    path('photo/', ListCreatePhotoAPIView.as_view()),
    path('photo/<int:photo_id>/', RetrieveUpdateDeletePhotoAPIView.as_view()),

    path('photos/<int:photo_id>/comments/', ListCreateCommentAPIView.as_view()),
    path('comment/<int:comment_id>', UpdateDeleteCommentAPIView.as_view()),

    path('photo/user/<int:user_id>/', ListUserPhotoAPIView.as_view()),
    path('photo/me/', ListCurrentUserPhotoAPIView.as_view()),
]

