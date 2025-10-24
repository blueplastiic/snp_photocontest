from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from django.conf import settings

from utils.paginator import CustomPagination

from drf_spectacular.utils import extend_schema

from service_objects.services import ServiceOutcome
from contest_api.services.photo import CreatePhotoService, RetrievePhotoService, DeletePhotoService, UpdatePhotoService, ListPhotoService, ListUserPhotoService, ListCurrentUserPhotoService
from contest_api.serializers.photo import ListPhotoSerializer, ListCurrentUserPhotoSerializer, RetrievePhotoSerializer, NewPhotoSerializer
from contest_api.docs.photo import (
    photos_list_docs,
    photo_create_docs,
    user_photos_list_docs,
    current_user_photos_list_docs,
    photo_retrieve_docs,
    photo_update_docs,
    photo_delete_docs
)

class ListCreatePhotoAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]
    
    @extend_schema(**photos_list_docs)
    def get(self,request):
        outcome: ServiceOutcome = ServiceOutcome(
            ListPhotoService, 
            request.query_params
        ) 

        return Response(
            {
                "pagination": CustomPagination(
                    page=outcome.result,
                    current_page = outcome.service.cleaned_data.get('page') or 1,
                    per_page = outcome.service.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
                ).to_json(),

                "results": ListPhotoSerializer(
                    outcome.result.object_list, #pyright:ignore
                    many=True
                ).data
            },
            status=status.HTTP_200_OK
        )
    @extend_schema(**photo_create_docs)
    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreatePhotoService,
            {
                **request.data, 'user': request.user
             },
            request.FILES
        )
        
        return Response(
            NewPhotoSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        )

class ListUserPhotoAPIView(APIView):
    permrssion_classes = [AllowAny]

    @extend_schema(**user_photos_list_docs)
    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            ListUserPhotoService,
            {
                **kwargs, **request.GET.dict()
            }
        )

        return Response(
            {
                "pagination": CustomPagination(
                    page=outcome.result,
                    current_page=outcome.service.cleaned_data.get('page') or 1,
                    per_page = outcome.service.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
                ).to_json(),
                
                "results":  ListPhotoSerializer(
                    outcome.result.object_list, #pyright: ignore
                    many=True
                ).data
            },
            status=status.HTTP_200_OK
        )


class ListCurrentUserPhotoAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(**current_user_photos_list_docs)
    def get(self,request):
        outcome: ServiceOutcome = ServiceOutcome(
            ListCurrentUserPhotoService,
            {
                'user': request.user, **request.GET.dict()
            }
        )

        return Response(
            {
                "pagination": CustomPagination(
                    page=outcome.result,
                    current_page=outcome.service.cleaned_data.get('page') or 1,
                    per_page=outcome.service.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE'],
                ).to_json(),
                "results": ListCurrentUserPhotoSerializer(
                    outcome.result.object_list, #pyright: ignore
                    many=True
                ).data
            },
            status=status.HTTP_200_OK
        )

class RetrieveUpdateDeletePhotoAPIView(APIView): 
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(**photo_retrieve_docs)
    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            RetrievePhotoService,
            kwargs
        )
        return Response(
            RetrievePhotoSerializer(outcome.result).data,
            status=status.HTTP_200_OK
        )

    @extend_schema(**photo_update_docs)
    def patch(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            UpdatePhotoService,
            {
                **kwargs,
                **request.data,
                'user': request.user
            },
            request.FILES
        )
        return Response(
            status=status.HTTP_200_OK
        )

    @extend_schema(**photo_delete_docs)
    def delete(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            DeletePhotoService,
            {
                **kwargs, 'user': request.user
            }
        )
        return Response(
            status=status.HTTP_200_OK
        )

