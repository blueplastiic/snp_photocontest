from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'


urlpatterns=[
    path('register/', views.UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='user_login'),
    path('<int:user_id>/', views.UserProfileAPIView.as_view(), name='user_profile'),
    path('<int:user_id>/settings/', views.UserSettingsAPIView.as_view(), name='user_settings')
]
