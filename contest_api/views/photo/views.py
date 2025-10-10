from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from service_objects.services import ServiceOutcome
from contest_api.services import CreatePhotoService, ListPhotoService, ListUserPhotoService, ListCurrentUserPhotoService, RetrievePhotoService
from contest_api.serializers import ListPhotoSerializer, ListCurrentUserPhotoSerializer, RetrievePhotoSerializer

class ListCreatePhotoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self,request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(ListPhotoService, kwargs) 

        return Response(
            ListPhotoSerializer(outcome.result, many=True).data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreatePhotoService,
            {
                **request.data, 'user': request.user
             },
            request.FILES
        )
        
        return Response(status=status.HTTP_201_CREATED)

class ListUserPhotoAPIView(APIView):
    permrssion_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            ListUserPhotoService,
            {
                **kwargs
            }
        )

        return Response(
            ListPhotoSerializer(outcome.result, many=True).data,
            status=status.HTTP_200_OK
        )


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
            status = status.HTTP_200_OK
        )

class RetrievePhotoAPIView(APIView): 
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            RetrievePhotoService,
            kwargs
        )
        return Response(
            RetrievePhotoSerializer(outcome.result).data,
            status=status.HTTP_200_OK
        )

