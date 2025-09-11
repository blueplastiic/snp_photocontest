from rest_framework.views import APIView

class UserRegisterAPIView(APIView):
    def post(self, request):
        request_serializer = UserRegisterSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        new_user = RegisterUserService.execute(request_serializer.validated_data)
        token = GetUserTokenService.execute({'user': new_user})

        response_data = {'id': new_user.id, 'token': token.key} #pyright: ignore
        response_serializer = UserGetTokenSerializer(response_data)

        return Response({'detail': response_serializer.data}) #pyright: ignore

