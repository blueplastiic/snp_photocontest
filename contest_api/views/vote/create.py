from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from service_objects.services import  ServiceOutcome
from contest_api.services import CreateVoteService

class CreateVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def create(self,request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateVoteService,
            {**request.data, 'user': request.user}
        )

