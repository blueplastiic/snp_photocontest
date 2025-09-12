from service_objects.services import Service
from users.models import User

class RegisterUserService(Service):
    def process(self): #change change change
        email = self.data['email']
        username = self.data['username']
        password = self.data['password']
        about = self.data.get('about', '')

        new_user = User.objects.create_user(email=email, username=username, password=password, about=about) #pyright: ignore
        return new_user.auth_token

