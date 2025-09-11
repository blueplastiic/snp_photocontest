from service_objects.services import Service

class ConfirmActionService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        password = self.data.get('password', None)
        if user and user.check_password(password):
            return True
        return False

