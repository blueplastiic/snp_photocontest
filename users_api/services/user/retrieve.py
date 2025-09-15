from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from django.conf import settings
from django import forms

class GetUserByIdService(ServiceWithResult):
    id = forms.IntegerField()

    def process(self): #pyright: ignore
        User = settings.AUTH_USER_MODEL
        id = self.cleaned_data.get('id')

        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            raise NotFound(additional_info='User does not exist')

        self.result = user
        return self

