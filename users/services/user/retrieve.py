from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from users.models import User
from django import forms

class GetUserByIdService(ServiceWithResult):
    id = forms.IntegerField()

    def process(self): #pyright: ignore
        id = self.cleaned_data.get('id')

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound(additional_info='User does not exist')

        self.result = user
        return self

