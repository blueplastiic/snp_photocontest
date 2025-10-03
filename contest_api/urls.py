from django.urls import path
from contest_api.views.photo import detail
from contest_api.views.photo import create
from contest_api.views.photo import user_photo_list

app_name = 'contest_api'

urlpatterns=[ 
    path('photo/<int:id>/', detail.PhotoDetailAPIView.as_view(), name='photo_create'),
    path('photo/create/', create.CreatePhotoAPIView.as_view(), name='photo_detail'),
    path('photo/list/<int:user_id>', user_photo_list.UserPhotosAPIView.as_view(), name='photo_list_user')
]

