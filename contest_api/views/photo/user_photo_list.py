from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from service_objects.services import ServiceOutcome
from contest_api.services import GetPhotoList
from contest_api.serializers import PhotoListSerializer

class UserPhotosAPIView(APIView, PageNumberPagination):
    permission_classes = [AllowAny]
    page_size = 3

    def get(self,request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            GetPhotoList,
            {
                **kwargs
            }
        )

        results = self.paginate_queryset(outcome.result, request, view=self)

        serializer = PhotoListSerializer(
            results, 
            many=True,
            context={'user': request.user}
        )

        return self.get_paginated_response(serializer.data) 

