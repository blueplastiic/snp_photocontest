from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from service_objects.services import ServiceOutcome
from contest_api.services import DeleteVoteService

class DeleteVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteVoteService,
            {
                **kwargs, 'user': request.user
            }
        )

