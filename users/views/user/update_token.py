from rest_framework.views import APIView

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

