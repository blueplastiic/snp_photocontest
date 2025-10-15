from django.urls import path

from users_api.views import UserAPIView, PrivateUserAPIView, CreateUserAPIView, UpdateTokenAPIView

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users_api'


urlpatterns=[
    path('register/', CreateUserAPIView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='user_login'),

    path('<int:id>/', UserAPIView.as_view(), name='user_profile'),

    path('me/', PrivateUserAPIView.as_view(), name='user_settings'),
    path('me/token/', UpdateTokenAPIView.as_view(), name='update_token'),
]

