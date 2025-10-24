from django.urls import path

from users_api.views.user import RetrieveUserAPIView, RetrieveUpdateDeleteUserAPIView, CreateUserAPIView
from users_api.views.token import UpdateTokenAPIView

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns=[ 
    path('register/', CreateUserAPIView.as_view()),
    path('login/', obtain_auth_token),

    path('users/<int:id>/', RetrieveUserAPIView.as_view()),
    
    path('me/', RetrieveUpdateDeleteUserAPIView.as_view()),
    path('me/token/', UpdateTokenAPIView.as_view(),) 
]

