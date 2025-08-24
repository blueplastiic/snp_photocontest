from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .services import *

class UserAPIView(APIView):
    def post(self, request):
        reg_serializer = UserRegisterSerializer(data=request.data)
        reg_serializer.is_valid(raise_exception=True)
        new_user = RegisterUserService.execute(reg_serializer.validated_data) 
        return Response({'user': UserGetSerializer(new_user).data}) #pyright: ignore
        #TODO: redirect to user's profile

