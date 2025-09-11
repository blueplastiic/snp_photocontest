from django.urls import path
from users.views.user import details, profile, register, update_token
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'users'


urlpatterns=[
    path('register/', register.UserRegisterAPIView.as_view(), name='user_register'),
    path('login/', obtain_auth_token, name='user_login'),
    path('<int:user_id>/', profile.UserProfileAPIView.as_view(), name='user_profile'),
    path('me/', details.UserDetailsAPIView.as_view(), name='user_settings'),
    path('me/token/', update_token.UserUpdateTokenAPIView.as_view(), name='update_token'),
]
