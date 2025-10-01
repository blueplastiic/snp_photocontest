from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from service_objects.services import Service, ServiceOutcome
from contest_api.services import CreateCommmentService

class CreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateCommmentService,
            {
                **kwargs, **request.data, 'user': request.user
            }
        )
        return Response(outcome.response_status)

