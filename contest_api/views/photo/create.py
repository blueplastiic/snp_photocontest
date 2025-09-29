from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from contest_api.services.photo import CreatePhotoService
from service_objects.services import ServiceOutcome

class CreatePhotoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreatePhotoService,
            {
                **request.data, 'user': request.user
             },
            request.FILES
        )
        
        return Response(status=status.HTTP_201_CREATED)

