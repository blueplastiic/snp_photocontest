from service_objects.services import Service
from rest_framework.authtoken.models import Token
from .models import User

class ConfirmActionService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        password = self.data.get('password', None)
        if user and user.check_password(password):
            return True
        return False

class RegisterUserService(Service):
    def process(self): #change change change
        email = self.data['email']
        username = self.data['username']
        password = self.data['password']
        about = self.data.get('about', '')

        new_user = User.objects.create_user(email=email, username=username, password=password, about=about) #pyright: ignore
        return new_user 

class GetUserTokenService(Service): 
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
            user = GetUserByIdService.execute({'user_id': user_id})

        token = self.get_token(user)
        return token

class CreateUserTokenService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User not authenticated')
        token,_ = Token.objects.get_or_create(user=user)
        return token

class DeleteUserTokenService(Service):
    def process(self):
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User cannot be found ')
        try: 
            token = Token.objects.get(user=user)
            token.delete()
        except Token.DoesNotExist:
            raise ValueError('Token not found')

class UpdateUserTokenService(Service): #transaction?
    def process(self):
        user = self.data.get('user', None)
        if not user:
            raise ValueError('User cannot be found')
        DeleteUserTokenService.execute({'user': user})
        new_token = CreateUserTokenService.execute({'user': user})
        return new_token

class GetUserByIdService(Service):
    def process(self): #pyright: ignore
        user_id = self.data['user_id']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise ValueError('Invalid id,user not found') #not sure about that one
        return user

class UpdatePublicUserInfoService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user')
        if not user:
            raise ValueError('User cannot be found')

        username = self.data.get('username')
        about = self.data.get('about')
        if not username and not about:
            raise ValueError('Data not provided')

        if username:
            user.username = username
        if about:
            user.about = about

        user.save()

class DeleteUserService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user', None)
        password = self.data.get('password', None)
        if ConfirmActionService.execute({'user':user, 'password': password}):
            user.delete()
            return True
        return False

