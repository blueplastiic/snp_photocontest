from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from service_objects.services import ServiceOutcome
from contest_api.services import CreatePhotoService, ListPhotoService, ListCurrentUserPhotoService, RetrievePhotoService
from contest_api.serializers import ListPhotoSerializer, ListCurrentUserPhotoSerializer, RetrievePhotoSerializer

class ListCreatePhotoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            ListPhotoService,
            {
                **kwargs, **request.data
            }
        )

        return Response(
            ListPhotoSerializer(outcome.result, many=True).data,
            status=outcome.response_status
        )

    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreatePhotoService,
            {
                **request.data, 'user': request.user
             },
            request.FILES
        )
        
        return Response(status=outcome.response_status)

class ListCurrentUserPhotoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            ListCurrentUserPhotoService,
            {
                'user': request.user
            }
        )

        return Response(
            ListCurrentUserPhotoSerializer(outcome.result, many=True).data,
            status = outcome.response_status
        )

class RetrievePhotoAPIView(APIView): 
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            RetrievePhotoService,
            kwargs
        )
        return Response(RetrievePhotoSerializer(outcome.result).data, status=outcome.response_status)
#TODO: delete photo (celery)

