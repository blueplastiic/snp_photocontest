from functools import lru_cache
from typing import Optional
from utils.statuses import PhotoStatus

from .base_list import BaseListPhotoService

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet 
from django import forms

from service_objects.errors import NotFound 

from models_app.models import Photo, User


class ListUserPhotoService(BaseListPhotoService):
    user_id = forms.IntegerField()
    custom_validations = ['user_presence']

    @property
    @lru_cache()
    def _user(self) -> Optional[User]:
        try:
            return User.objects.get(
                id=self.cleaned_data.get('user_id')
            )
        except ObjectDoesNotExist:
            return None

    @property
    def _photos(self) -> QuerySet[Photo]:
        photos = super()._photos
        return photos.filter(user=self._user)

    @property
    def _filtered_photos(self) -> QuerySet[Photo]:
        photos =super()._photos
        return photos.filter(status=PhotoStatus.APPROVED)

    def user_presence(self) -> None:
        if self.cleaned_data.get('user_id') and not self._user:
            self.add_error(
                'user_id',
                NotFound(
                    message=f"User {self.cleaned_data['user_id']} not found"
                )
            )

