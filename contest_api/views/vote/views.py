from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from service_objects.services import  ServiceOutcome
from contest_api.services.vote import CreateVoteService, DeleteVoteService

from drf_spectacular.utils import extend_schema

from contest_api.docs.vote import votes_create_docs, votes_delete_docs

class CreateVoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**votes_create_docs)
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

    @extend_schema(**votes_delete_docs)
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

