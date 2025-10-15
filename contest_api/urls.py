from django.urls import path

from contest_api.views.comment.views import ListCreateCommentAPIView, UpdateDeleteCommentAPIView
from contest_api.views.photo.views import ListCreatePhotoAPIView, ListCurrentUserPhotoAPIView, ListUserPhotoAPIView, RetrievePhotoAPIView

app_name = 'contest_api'

urlpatterns=[ 

    path('comment/', ListCreateCommentAPIView.as_view(), name='comment_create'),
    path('comment/<int:comment_id>', UpdateDeleteCommentAPIView.as_view(), name='comment_actions'),

    path('photo/', ListCreatePhotoAPIView.as_view(), name='photo_list_create'),
    path('photo/<int:photo_id>/', RetrievePhotoAPIView.as_view(), name='photo_retrieve'),

    path('photo/user/<int:user_id>/', ListUserPhotoAPIView.as_view(), name='photo_list_user'),
    path('photo/me/', ListCurrentUserPhotoAPIView.as_view(), name='photo_list_current_user'),
]

