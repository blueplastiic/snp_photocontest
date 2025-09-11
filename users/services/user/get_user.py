from service_objects.services import Service
from users.models import User

class GetUserByIdService(Service):
    def process(self): #pyright: ignore
        user_id = self.data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError('Invalid id,user not found') #not sure about that one
        return user

