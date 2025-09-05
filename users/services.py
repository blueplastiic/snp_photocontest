from service_objects.services import Service
from rest_framework.authtoken.models import Token
from .models import User

class RegisterUserService(Service):
    def process(self):
        email = self.data['email']
        username = self.data['username']
        password = self.data['password']
        about = self.data.get('about', '')

        new_user = User.objects.create_user(email=email, username=username, password=password, about=about) #pyright: ignore
        return new_user 


class GetUserService(Service):
    def process(self): #pyright: ignore
        user_id = self.data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError('Invalid id,user not found') #not sure about that one
        return user

class GetUserTokenService(Service): #THIS MAKES ME REALLY PROUD OF MYSELF
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
            user = GetUserService.execute({'user_id': user_id})

        token = self.get_token(user)
        return token
        



