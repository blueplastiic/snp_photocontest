from functools import lru_cache
from typing import Optional, Self

from django.core.exceptions import ObjectDoesNotExist
from django import forms

from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, Photo


class DeletePhotoService(ServiceWithResult):
    user = ModelField(User)
    photo_id = forms.IntegerField()

    custom_validations = ['photo_presence']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.delete_photo()
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        try:
            return (Photo.objects
                    .get(id= self.cleaned_data['photo_id'], user=self._user)
                    )

        except ObjectDoesNotExist:
            return None

    def delete_photo(self):
        pass

    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                'photo_id',
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

