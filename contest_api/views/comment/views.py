from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_spectacular.utils import extend_schema

from service_objects.services import ServiceOutcome

from contest_api.services.comment import CreateCommmentService, DeleteCommentService, ListCommentService, UpdateCommentService
from contest_api.serializers.comment import ParentCommentSerializer, NewCommentSerializer
from contest_api.docs.comment import(
    comments_list_docs,
    comments_create_docs,
    comments_delete_docs,
    comments_update_docs
)

class ListCreateCommentAPIView(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(**comments_list_docs)
    def get(self, request, *args, **kwargs): 
        outcome: ServiceOutcome = ServiceOutcome(
            ListCommentService,
            {
                **kwargs
            }
        )
        return Response(
            ParentCommentSerializer(outcome.result, many=True).data,
            status=status.HTTP_200_OK
        ) 

    @extend_schema(**comments_create_docs)
    def post(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateCommmentService,
            {
                **kwargs,
                **request.data,
                'user': request.user
            }
        )
        return Response(
            NewCommentSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        ) 

class UpdateDeleteCommentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**comments_update_docs)
    def patch(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            UpdateCommentService,
            {
                **kwargs,
                **request.data, 
                'user': request.user
            }
        )

        return Response(status=status.HTTP_200_OK)

    @extend_schema(**comments_delete_docs)
    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteCommentService,
            {
                **kwargs, 
                'user': request.user
            }
        )
        
        return Response(status=status.HTTP_200_OK)

