from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from service_objects.services import ServiceOutcome
from contest_api.services import GetPhotoByIdService
from contest_api.serializers.photo import PhotoDetailSerializer

class PhotoDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            GetPhotoByIdService,
            kwargs
        )
        return Response(PhotoDetailSerializer(outcome.result).data, status=status.HTTP_200_OK)

