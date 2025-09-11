from service_objects.services import Service
from rest_framework.authtoken.models import Token
from get_user import GetUserByIdService

class GetTokenService(Service): 
    def get_token(self, user):
        try:
            token = Token.objects.get(user=user) 
        except Token.DoesNotExist:
            raise ValueError('Token not found')
        return token

    def process(self): #pyright: ignore
        user_id = self.data.get('user_id', None)
        user = self.data.get('user', None)
        if not user:
            user = GetUserByIdService.execute({'user_id': user_id})

        token = self.get_token(user)
        return token

