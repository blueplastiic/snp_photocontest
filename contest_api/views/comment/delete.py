from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from contest_api.services import DeleteCommentService

class DeleteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteCommentService,
            {
                **kwargs, 'user': request.user
            }
        )
        
        return Response(outcome.response_status)
   
