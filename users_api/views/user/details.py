from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from users_api.services.user.update_public import UpdatePublicInfoService
from users_api.services.user.delete import DeleteUserService
from users_api.serializers.user.retrieve_private import UserPrivateSerializer
from service_objects.services import ServiceOutcome

class UserDetailsAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserPrivateSerializer(request.user).data)

    def patch(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            UpdatePublicInfoService,
            {**request.data, 'user': request.user}
        )
        return Response(UserPrivateSerializer(outcome.result).data, status.HTTP_200_OK)
        
    def delete(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            DeleteUserService, 
            {'user':request.user}
        )
        return Response(status=outcome.response_status) 

