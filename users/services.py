from service_objects.services import Service
from .models import User

class RegisterUserService(Service):
    def process(self):
        email = self.data['email']
        username = self.data['username']
        password = self.data['password']
        about = self.data.get('about', '')

        new_user = User.objects.create_user(email=email, username=username, password=password, about=about) #pyright: ignore
        return new_user 

class GetUserProfileService(Service):
    def process(self): #pyright: ignore
        user_id = self.data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError('Invalid id,user not found') #not sure about that one
        return user       
