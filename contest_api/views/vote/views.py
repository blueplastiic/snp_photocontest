from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from service_objects.services import  ServiceOutcome
from contest_api.services.vote import CreateVoteService, DeleteVoteService

class CreateVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request, *arg, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateVoteService,
            {
                **request.data, 
                'user': request.user
            }
        )
        
        return Response(outcome.response_status)

class DeleteVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteVoteService,
            {
                **kwargs, 
                **request.data, 
                'user': request.user
            }
        )
        return Response(outcome.response_status)
