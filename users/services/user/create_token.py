from service_objects.services import Service
from rest_framework.authtoken.models import Token

class CreateTokenService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User not authenticated')
        token,_ = Token.objects.get_or_create(user=user)
        return token

