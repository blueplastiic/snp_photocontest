from django.urls import path
from users_api.views.user import details, profile, register
from users_api.views.token import update
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users_api'


urlpatterns=[
    path('register/', register.UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='user_login'),
    path('<int:id>/', profile.UserProfileAPIView.as_view(), name='user_profile'),
    path('me/', details.UserDetailsAPIView.as_view(), name='user_settings'),
    path('me/token/', update.UpdateTokenAPIView.as_view(), name='update_token'),
]

