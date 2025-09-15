from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from django.conf import settings

class DeleteUserService(ServiceWithResult):
    User = settings.AUTH_USER_MODEL
    user = ModelField(User)

    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        user.delete() #pyright: ignore
        return self

