from functools import lru_cache
from typing import Self, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django import forms
from django.db.models import Count

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound

from models_app.models import Photo, User

class ListUserPhotoService(ServiceWithResult):
    user_id = forms.IntegerField()

    custom_validations = ['user_presence']
    
    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.list_user_photo()
        return self

    @property
    @lru_cache()
    def _user(self) -> Optional[User]:
        try:
            return User.objects.get(
                id=self.cleaned_data.get('user_id')
            )
        except ObjectDoesNotExist:
            return None

    def user_presence(self) -> None:
        if self.cleaned_data.get('user_id'):
            if not self._user:
                self.add_error(
                    'user_id',
                    NotFound(
                        message=f"User {self.cleaned_data['user_id']} not found"
                    )
                )

    def list_user_photo(self) -> QuerySet:
        return (
            Photo.objects
            .annotate(
                num_comments=Count('comments'),
                num_votes=Count('votes')
                      )
            .filter(user=self._user)
        )

