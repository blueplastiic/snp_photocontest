from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from models_app.models import User

class DeleteUserService(ServiceWithResult):
    user = ModelField(User)

    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        user.delete() #pyright: ignore
        return self

