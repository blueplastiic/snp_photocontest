from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from users_api.services.token.update import UpdateTokenService
from users_api.serializers.token.update import UpdateTokenSerializer

from rest_framework import status
from service_objects.services import ServiceOutcome

from drf_spectacular.utils import extend_schema
from users_api.docs.token import user_update_docs

class UpdateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**user_update_docs)
    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            UpdateTokenService,
            {
                'user': request.user
            }
        )
        return Response(
            UpdateTokenSerializer(outcome.result).data,
            status.HTTP_200_OK
        )

