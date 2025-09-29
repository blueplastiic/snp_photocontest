from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from models_app.models import User

from rest_framework.authtoken.models import Token

class UpdateTokenService(ServiceWithResult):
    
    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        
        Token.objects.get(user=user).delete()
        Token.objects.create(user=user)
        
        self.result = user
        return self

