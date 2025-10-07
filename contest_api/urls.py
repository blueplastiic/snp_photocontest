from django.urls import path

from contest_api.views.photo.create import CreatePhotoAPIView
from contest_api.views.photo.detail import PhotoDetailAPIView

from contest_api.views.vote.views import VoteAPIView

from contest_api.views.comment.create import CreateCommentAPIView
from contest_api.views.comment.actions import CommentActionsAPIView

app_name = 'contest_api'

urlpatterns=[ 
    path('photo/create/', CreatePhotoAPIView.as_view(), name='photo_create'),
    path('photo/<int:photo_id>/', PhotoDetailAPIView.as_view(), name='photo_detail'),
    path('photo/<int:photo_id>/vote', VoteAPIView.as_view(), name='vote'),

    path('comment/', CreateCommentAPIView.as_view(), name='comment_create'),
    path('comment/<int:comment_id>', CommentActionsAPIView.as_view(), name='comment_actions'),
]

