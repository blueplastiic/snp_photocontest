from django.urls import path

from contest_api.views.vote.views import CreateVoteAPIView, DeleteVoteAPIView
from contest_api.views.comment.views import ListCreateCommentAPIView, UpdateDeleteCommentAPIView
from contest_api.views.photo.views import ListCreatePhotoAPIView, ListCurrentUserPhotoAPIView, ListUserPhotoAPIView, RetrieveUpdateDeletePhotoAPIView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns=[ 

     path('vote/', CreateVoteAPIView.as_view(), name='vote_create'),
     path('vote/<int:photo_id>/', DeleteVoteAPIView.as_view(), name='vote_delete'),
    
     path('comment/', ListCreateCommentAPIView.as_view(), name='comment_create'),
     path('comment/<int:comment_id>', UpdateDeleteCommentAPIView.as_view(), name='comment_actions'),
    
     path('photo/', ListCreatePhotoAPIView.as_view(), name='photo_list_create'),
     path('photo/<int:photo_id>/', RetrieveUpdateDeletePhotoAPIView.as_view()),
    
     path('photo/user/<int:user_id>/', ListUserPhotoAPIView.as_view(), name='photo_list_user'),
     path('photo/me/', ListCurrentUserPhotoAPIView.as_view(), name='photo_list_current_user'),
    
]

urlpatterns+=[
    path('docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui')
]

