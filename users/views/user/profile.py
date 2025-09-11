from rest_framework.views import APIView

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

