from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users_api.services.token import UpdateTokenService
from users_api.serializers.token import RetrieveTokenSerializer

from rest_framework import status
from service_objects.services import ServiceOutcome

class UpdateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            UpdateTokenService,
            {'user': request.user}
        )
        return Response(
            RetrieveTokenSerializer(outcome.result).data, 
            status.HTTP_200_OK
        )

