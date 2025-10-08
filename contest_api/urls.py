from django.urls import path
from contest_api.views.photo import views

app_name = 'contest_api'

urlpatterns=[ 

    path('photo/', views.ListCreatePhotoAPIView.as_view(), name='photo_list_create'),
    path('photo/me/', views.ListCurrentUserPhotoAPIView.as_view(), name='photo_list_current_user'),
    path('photo/<int:photo_id>/', views.RetrievePhotoAPIView.as_view(), name='photo_retrieve'),
]

