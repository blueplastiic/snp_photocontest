from typing import Self, Optional
from functools import lru_cache
from utils.statuses import PhotoStatus

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField

from models_app.models import Photo, PhotoHistory, User

from django.core.exceptions import ObjectDoesNotExist
from django import forms


class UpdatePhotoService(ServiceWithResult):
    user = ModelField(User)
    photo_id = forms.IntegerField()

    new_title = forms.CharField(max_length=100, required=False)
    new_description = forms.CharField(max_length=300, required=False)
    new_image = forms.ImageField(required=False)

    custom_validations = ['photo_presence', 'data_provided']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.update_data()
        return self

    @property
    @lru_cache()
    def _user(self) -> User: 
        return self.cleaned_data['user']

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        try:
            return Photo.objects.get(
                id=self.cleaned_data['photo_id'],
                user=self._user
            )
        except ObjectDoesNotExist:
            return None

    def update_data(self) -> None:
        if self.cleaned_data.get('new_image'):
            self.update_image()

        if self.cleaned_data.get('new_title'):
            self.update_title()

        if self.cleaned_data.get('new_description'):
            self.update_description()

        self._photo.status = PhotoStatus.PENDING # pyright: ignore
        self._photo.save() #pyright: ignore

    def update_image(self) -> None:
        PhotoHistory.objects.create(
            model=self._photo,
            old_image=self._photo.image #pyright:ignore
        )
        self._photo.image = self.cleaned_data.get('new_image') #pyright:ignore

    def update_title(self) -> None:
        self._photo.title = self.cleaned_data.get('new_title') #pyright: ignore

    def update_description(self) -> None:
        self._photo.description = self.cleaned_data.get('new_description') #pyright: ignore

    def photo_presence(self):
        if not self._photo:
            self.add_error(
                'photo_id',
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

    def data_provided(self) -> None:        
        new_title = self.cleaned_data.get('new_title')
        new_description =self.cleaned_data.get('new_description')
        new_image = self.cleaned_data.get('new_image')
       
        #i dont like it
        if not new_title and not new_description and not new_image:
            self.add_error(
                'new_title',
                ValidationError(
                    message="No data provided"
                )
            )
            self.add_error(
                'new_description',
                ValidationError(
                    message="No data provided"
                )
            )
            self.add_error(
                'new_image',
                ValidationError(
                    message="No data provided"
                )
            )

