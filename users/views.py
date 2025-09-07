from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .services import *

class UserRegisterAPIView(APIView):
    def post(self, request):
        request_serializer = UserRegisterSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        new_user = RegisterUserService.execute(request_serializer.validated_data)
        token = GetUserTokenService.execute({'user': new_user})

        response_data = {'id': new_user.id, 'token': token.key} #pyright: ignore
        response_serializer = UserGetTokenSerializer(response_data)

        return Response({'detail': response_serializer.data}) #pyright: ignore

class UserUpdateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request): #not sure about the http-method
        user = request.user
        try:
            new_token = UpdateUserTokenService.execute({'user': user})
        except ValueError:
            return Response(data={'error': 'User cannot be found'},status=status.HTTP_404_NOT_FOUND)

        response_data = {'id': user.id, 'token': new_token.key} #pyright: ignore
        response_serializer = UserGetTokenSerializer(response_data)

        return Response({'detail': response_serializer.data})

class UserProfileAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        if not user_id:
            return Response({'error': 'User id missing'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = GetUserByIdService.execute({'user_id': user_id})
        except ValueError:
            return Response(data={'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': UserPublicSerializer(user).data})

class UserDetailsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserPrivateSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        request_serializer = UserPublicSerializer(data=request.data, partial=True)
        request_serializer.is_valid(raise_exception=True)

        username = request_serializer.validated_data.get('username', None) #pyright: ignore
        about = request_serializer.validated_data.get('about', None) #pyright: ignore

        try:
            UpdatePublicUserInfoService.execute({'username': username, 'about': about, 'user': request.user})
            return Response({'detail': 'User data updated'})
        except ValueError:
            return Response({'detail': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        serializer = UserConfirmActionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        entered_password = serializer.validated_data['password'] #pyright: ignore 

        if DeleteUserService.execute({'user': request.user, 'password': entered_password}):
            return Response({'detail': 'You have deleted your account'}) 
        else:
            return Response(data={'detail': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

