from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.services.token.update import UpdateTokenService
from users.serializers.token.retrieve import TokenSerializer
from rest_framework import status

class UpdateTokenAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            token = UpdateTokenService.execute(request.data)
        except ValueError:
            return Response(data={'error': 'User cannot be found'},status=status.HTTP_404_NOT_FOUND)
        
        return Response(TokenSerializer(token).data)

