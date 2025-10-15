from typing import Self
from functools import lru_cache

from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError
from service_objects.fields import ModelField


from models_app.models import Photo, User
from django import forms
from utils.statuses import PhotoStatus


class CreatePhotoService(ServiceWithResult):
    user = ModelField(User)
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)
    photo = forms.ImageField()

    custom_validations = ['name_dup']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.create_photo()
        return self

    @property
    @lru_cache()
    def _user(self) -> User: 
        return self.cleaned_data['user']

    def name_dup(self) -> None:
        photo_exists = Photo.objects.filter(
            user=self._user,
            title=self.cleaned_data['title']
        ).exists()

        if photo_exists:
            self.add_error(
                'title',
                ValidationError(
                    message=f"You already have a photo with title {self.cleaned_data['title']}"
                )
            )

    def create_photo(self) -> Photo:
        new_photo = Photo.objects.create(
            user=self._user,
            title=self.cleaned_data['title'],
            description=self.cleaned_data['description'],
            photo = self.cleaned_data['photo'],
            status = PhotoStatus.PENDING
        )
        return new_photo

