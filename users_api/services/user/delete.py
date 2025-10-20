from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User


class DeleteUserService(ServiceWithResult):
    user = ModelField(User)

    def process(self): #pyright: ignore
        if self.is_valid():
            self.delete_user()
        return self

    def delete_user(self):
        user = self.cleaned_data['user']
        user.delete()

