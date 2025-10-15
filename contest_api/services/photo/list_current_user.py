from functools import lru_cache
from .base_list import BaseListPhotoService

from utils.statuses import PhotoStatus

from django.db.models import QuerySet
from django import forms

from service_objects.fields import ModelField

from models_app.models import Photo, User


class ListCurrentUserPhotoService(BaseListPhotoService):
    user = ModelField(User)
    status = forms.ChoiceField(choices=PhotoStatus.STATUS_CHOICES, required=False)

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    @property
    def _photos(self) -> QuerySet[Photo]:
        photos = super()._photos
        return photos.filter(user=self._user)

    @property
    def _filtered_photos(self) -> QuerySet[Photo]:
        status = self.cleaned_data.get('status')

        photos = super()._filtered_photos
        if status:
            photos = photos.filter(status=status)
        return photos

