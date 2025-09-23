from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from contest_api.services.photo import CreatePhotoService
from service_objects.services import ServiceOutcome

class CreatePhotoAPIView(APIView):
    def post(self, request):
        request.data['user'] = request.user
        outcome: ServiceOutcome = ServiceOutcome(
            CreatePhotoService,
            request.data
        )
        
        return Response(status=status.HTTP_201_CREATED)

