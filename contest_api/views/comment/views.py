from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from service_objects.services import ServiceOutcome

from contest_api.services import CreateCommmentService, DeleteCommentService, ListCommentService, UpdateCommentService
from contest_api.serializers.comment import ParentCommentSerializer, NewCommentSerializer


class ListCreateCommentAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateCommmentService,
            {
                **kwargs, **request.data, 'user': request.user
            }
        )
        return Response(
            NewCommentSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        ) 

    def get(self, request): 
        outcome: ServiceOutcome = ServiceOutcome(
            ListCommentService,
            {
                **request.data
            }
        )
        return Response(
            ParentCommentSerializer(outcome.result, many=True).data,
            status=status.HTTP_200_OK
        ) 

class UpdateDeleteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteCommentService,
            {
                **kwargs, 'user': request.user
            }
        )
        
        return Response(status=status.HTTP_200_OK)

    def update(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            UpdateCommentService,
            {
                **request.data, 'user': request.user
            }
        )

        return Response(status=status.HTTP_200_OK)

