from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from users_api.services.user import CreateUserService, DeleteUserService, RetrieveUserService, UpdatePublicInfoUserService
from users_api.serializers.user import PublicUserSerializer, PrivateUserSerializer
from users_api.serializers.token import RetrieveTokenSerializer

from drf_spectacular.utils import extend_schema

from users_api.docs.user import (
    user_public_retrieve_docs, 
    user_private_retrieve_docs,
    user_update_docs, 
    user_delete_docs,
    user_create_docs,
    user_login_docs
)

from service_objects.services import ServiceOutcome


class RetrieveUserAPIView(APIView): #naming troubles again
    permission_classes = [AllowAny]

    @extend_schema(**user_public_retrieve_docs)
    def get(self, request, *args, **kwargs):
        outcome: ServiceOutcome = ServiceOutcome(
            RetrieveUserService, 
            {
                **kwargs
            }
        )

        return Response(
            PublicUserSerializer(outcome.result).data, 
            status.HTTP_201_CREATED
        )

class RetrieveUpdateDeleteUserAPIView(APIView): #naming troubles again

    permission_classes = [IsAuthenticated]
    
    #what da dog doin
    @extend_schema(**user_private_retrieve_docs)
    def get(self, request):
        return Response(PrivateUserSerializer(request.user).data)

    @extend_schema(**user_update_docs)
    def patch(self, request):
        request.data['user'] = request.user
        outcome: ServiceOutcome = ServiceOutcome(
            UpdatePublicInfoUserService,
            {
                **request.data
            }
        )
        return Response(
            PrivateUserSerializer(outcome.result).data,
            status.HTTP_200_OK
        )
    
    @extend_schema(**user_delete_docs)
    def delete(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteUserService, 
            {
                'user': request.user
            }
        )

        return Response(
            status=outcome.response_status
        ) 

class CreateUserAPIView(APIView):

    @extend_schema(**user_create_docs)
    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            CreateUserService, 
            {
                **request.data
            }
        )

        return Response(
            RetrieveTokenSerializer(outcome.result).data,
            status=status.HTTP_201_CREATED
        )

class LoginUserAPIView(ObtainAuthToken):

    @extend_schema(**user_login_docs)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
