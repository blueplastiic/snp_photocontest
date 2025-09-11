from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from serializers.user import 

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

