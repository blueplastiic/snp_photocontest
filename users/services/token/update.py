from service_objects.services import Service
from delete import DeleteTokenService 
from create import CreateTokenService

class UpdateTokenService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User cannot be found')
        DeleteTokenService.execute({'user': user})
        new_token = CreateTokenService.execute({'user': user})
        response_data = {
            'id': user.id,
            'auth_token': new_token.key #pyright: ignore
                         }
        return  response_data

