from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from service_objects.services import ServiceOutcome
from contest_api.services import CreatePhotoService, ListPhotoService, ListCurrentUserPhotoService, RetrievePhotoService
from contest_api.serializers import PhotoListSerializer, PhotoDetailSerializer

class ListCreatePhotoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            ListPhotoService,
            {
                **kwargs, **request.data
            }
        )

        # to be continued
        return None

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
    permission_classes = [AllowAny]

    def get(self,request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            ListCurrentUserPhotoService,
            {
                'user': request.user
            }
        )
        # to be continued
        return None

class RetrievePhotoAPIView(APIView): 
    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            RetrievePhotoService,
            kwargs
        )
        return Response(PhotoDetailSerializer(outcome.result).data, status=outcome.response_status)
#TODO: delete photo (celery)

