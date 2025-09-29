from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from users_api.services.user.retrieve import GetUserByIdService
from service_objects.services import ServiceOutcome
from users_api.serializers.user.retrieve_public import UserPublicSerializer

class UserProfileAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            GetUserByIdService, 
            kwargs
        )

        return Response(UserPublicSerializer(outcome.result).data, status.HTTP_200_OK)

