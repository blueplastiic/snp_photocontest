from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .services import *

class UserRegisterAPIView(APIView):
    def post(self, request):
        reg_serializer = UserRegisterSerializer(data=request.data)
        reg_serializer.is_valid(raise_exception=True)
        new_user = RegisterUserService.execute(reg_serializer.validated_data) 
        return Response({'user': UserGetSerializer(new_user).data}) #pyright: ignore

class UserLoginAPIView(APIView):
    def post(self,request):
        pass


class UserProfileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass

class UserSettingsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass
