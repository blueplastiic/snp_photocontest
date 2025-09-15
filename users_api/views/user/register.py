from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users_api.services.user.create import RegisterUserService
from users_api.serializers.token.retrieve import TokenSerializer
from service_objects.services import ServiceOutcome

class UserRegisterAPIView(APIView):
    def post(self, request):
        outcome: ServiceOutcome = ServiceOutcome(
            RegisterUserService, 
            request.data
        )
        
        return Response(TokenSerializer(outcome.result).data, status=status.HTTP_201_CREATED)

