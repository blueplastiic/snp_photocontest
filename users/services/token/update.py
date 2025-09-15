from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from users.models import User
from rest_framework.authtoken.models import Token

class UpdateTokenService(ServiceWithResult):
    user = ModelField(User)
    
    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        
        Token.objects.get(user=user).delete()
        Token.objects.create(user=user)
        
        self.result = user
        return self

