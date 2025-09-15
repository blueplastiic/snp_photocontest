from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from django.conf import settings

from rest_framework.authtoken.models import Token

class UpdateTokenService(ServiceWithResult):
    user = ModelField(settings.AUTH_USER_MODEL)
    
    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        
        Token.objects.get(user=user).delete()
        Token.objects.create(user=user)
        
        self.result = user
        return self

