from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from service_objects.services import ServiceOutcome
from users_api.services.user import CreateUserService, DeleteUserService, RetrieveUserService, UpdatePublicInfoUserService
from users_api.serializers.user import PublicUserSerializer, PrivateUserSerializer
from users_api.serializers.token import RetrieveTokenSerializer

class RetrieveUserAPIView(APIView): #naming troubles again
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            RetrieveUserService, 
            kwargs
        )

        return Response(
            PublicUserSerializer(outcome.result).data, 
            status.HTTP_201_CREATED
        )

class RetrieveUpdateDeleteUserAPIView(APIView): #naming troubles again

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(PrivateUserSerializer(request.user).data)

    def patch(self, request):
        request.data['user'] = request.user
        outcome: ServiceOutcome = ServiceOutcome(
            UpdatePublicInfoUserService,
            request.data
        )
        return Response(
            PrivateUserSerializer(outcome.result).data,
            status.HTTP_200_OK
        )
        
    def delete(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteUserService, 
            {'user':request.user}
        )

        return Response(
            status=outcome.response_status
        ) 

class CreateUserAPIView(APIView):
    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateUserService, 
            request.data
        )

        return Response(
            RetrieveTokenSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        )

class LoginUserAPIView(ObtainAuthToken):
    pass
