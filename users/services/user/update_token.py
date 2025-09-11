from service_objects.services import Service
from delete_token import DeleteTokenService 
from create_token import CreateTokenService

class UpdateUserTokenService(Service): #transaction?
    def process(self):
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User cannot be found')
        DeleteTokenService.execute({'user': user})
        new_token = CreateTokenService.execute({'user': user})
        return new_token

