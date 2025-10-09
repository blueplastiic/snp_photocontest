from typing import Self, Optional

from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import User

from django import forms
from django.core.exceptions import ObjectDoesNotExist

class RetrieveUserService(ServiceWithResult):
    user_id = forms.IntegerField()

    custom_validations = ['user_presence']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._user
        return self

    @property
    def _user(self) -> Optional[User]:
        try:
            return User.objects.get(
                id = self.cleaned_data['user_id']
            )
        except ObjectDoesNotExist:
            return None
            

    def user_presence(self) -> None:
        if not self._user:
            self.add_error(
                'user_id',
                NotFound(
                    message=f"User {self.cleaned_data['user_id']} does not exist"
                )
            )

