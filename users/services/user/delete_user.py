from service_objects.services import Service
from confirm_action import ConfirmActionService

class DeleteUserService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        password = self.data.get('password', None)
        if ConfirmActionService.execute({'user':user, 'password': password}):
            user.delete()
            return True
        return False

