from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users.services.user.update_public import UpdatePublicUserInfoService
from users.services.user.delete import DeleteUserService
from users.serializers.user.retrieve_private import UserPrivateSerializer

class UserDetailsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserPrivateSerializer(request.user).data)

    def patch(self, request):
        try:
            UpdatePublicUserInfoService.execute(request.data)
            return Response({'detail': 'Data updated'})
        except ValueError:
            return Response({'detail': 'Invalid data provided'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):

        if DeleteUserService.execute(request.data):
            return Response({'detail': 'You have deleted your account'}) 
        else:
            return Response(data={'detail': 'Incorrect password'}, status=status.HTTP_400_BAD_REQUEST)

