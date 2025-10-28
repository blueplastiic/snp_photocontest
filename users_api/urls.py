from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken

from users_api.views.user import (
    RetrieveUserAPIView,
    RetrieveUpdateDeleteUserAPIView,
    CreateUserAPIView,
    LoginUserAPIView
)

from users_api.views.token import UpdateTokenAPIView


app_name = 'users_api'


urlpatterns=[
    path('register/', CreateUserAPIView.as_view()),
    path('login/', LoginUserAPIView.as_view()),

    path('user/<int:id>/', RetrieveUserAPIView.as_view()),

    path('me/', RetrieveUpdateDeleteUserAPIView.as_view()),
    path('me/token/', UpdateTokenAPIView.as_view()),
]

