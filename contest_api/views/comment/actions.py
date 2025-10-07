from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from service_objects.services import ServiceOutcome
from contest_api.services import DeleteCommentService
from contest_api.services.comment.create import CreateCommmentService

class CommentActionsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    #author of the comment can delete it with this method
    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteCommentService,
            {
                **kwargs, 'user': request.user
            }
        )
        
        return Response(outcome.response_status)
  
#TODO: UPDATE

