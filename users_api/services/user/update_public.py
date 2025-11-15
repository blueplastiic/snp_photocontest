from typing import Self
from functools import lru_cache

from django import forms

from models_app.models import User

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import ValidationError


class UpdatePublicInfoUserService(ServiceWithResult):
    user = ModelField(User)
    username = forms.CharField(max_length=30, required=False)
    about = forms.CharField(max_length=500, required=False)

    custom_validations=['data_provided']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.update_data()
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    def update_data(self) -> None:
        if self.cleaned_data.get('username'):
            self.update_username()

        if self.cleaned_data.get('about'):
            self.update_about()
        
        self._user.save()

    def update_username(self) -> None:
        self._user.username = self.cleaned_data['username']

    def update_about(self) -> None:
        self._user.about = self.cleaned_data['about']

    def data_provided(self) -> None:
        if not self.cleaned_data.get('username') and not self.cleaned_data.get('about'):
            self.add_error(
                'username',
                ValidationError(
                    message="Neither username nor about field was provided"
                )
            )
            self.add_error(
                'about',
                ValidationError(
                    message="Neither username nor about field was provided"
                )
            )

