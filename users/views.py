from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import *
from .serializers import *
from .services import *

class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_user = RegisterUserService.execute(serializer.validated_data)
        token = GetUserTokenService.execute({'user': new_user})

        response_data = {'id': new_user.id, 'token': token} #pyright: ignore
        response_serializer = UserRegisterCompletedSerializer(response_data)

        return Response({'User': response_serializer.data}) #pyright: ignore

class UserProfileAPIView(APIView):

    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        if not user_id:
            return Response({'Error': 'User id missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = GetUserByIdService.execute({'user_id': user_id})
        except ValueError:
            return Response(data={'Error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'User': UserPublicGetSerializer(user).data})

class UserSettingsAPIView(APIView):

    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def delete(self, request, *args, **kwargs):
        pass
