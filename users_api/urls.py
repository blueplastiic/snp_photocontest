from django.urls import path

from users_api.views.user import RetrieveUserAPIView, RetrieveUpdateDeleteUserAPIView, CreateUserAPIView
from users_api.views.token import UpdateTokenAPIView

from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users_api'


urlpatterns=[
    path('register/', CreateUserAPIView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='user_login'),

    path('user/<int:id>/', RetrieveUserAPIView.as_view(), name='user_profile'),

    path('me/', RetrieveUpdateDeleteUserAPIView.as_view(), name='user_settings'),
    path('me/token/', UpdateTokenAPIView.as_view(), name='update_token'),
]

