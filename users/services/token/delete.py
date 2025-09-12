from service_objects.services import Service
from rest_framework.authtoken.models import Token

class DeleteTokenService(Service):
    def process(self):
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User cannot be found ')
        try: 
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            raise ValueError('Token not found')

