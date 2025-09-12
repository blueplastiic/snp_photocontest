from rest_framework.views import APIView
from rest_framework import status
from users.services.user.register import RegisterUserService
from users.serializers.token.retrieve import TokenSerializer

class UserRegisterAPIView(APIView):
    def post(self, request):
        new_user = RegisterUserService.execute(request.data)
        return Response(TokenSerializer(new_user).data) #pyright: ignore

