from functools import lru_cache
from typing import Self, Optional

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from django import forms
from django.db.models import Count
from django.core.paginator import Paginator, Page, EmptyPage
from django.conf import settings

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound

from models_app.models import Photo, User


class ListUserPhotoService(ServiceWithResult):
    user_id = forms.IntegerField()
    page=forms.IntegerField(required=False)
    per_page=forms.IntegerField(required=False)

    custom_validations = ['user_presence']
    
    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.paginated_photos
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

    @property
    def user_photos(self) -> QuerySet:
        return (
            Photo.objects
            .annotate(
                num_comments=Count('comments'),
                num_votes=Count('votes')
                      )
            .filter(user=self._user)
        )

    @property
    def paginated_photos(self) -> Page:
        try:
            return Paginator(
                object_list=self.user_photos,
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(self.cleaned_data.get('page') or 1)
        except EmptyPage:
            return Paginator(
                object_list=self.user_photos,
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(1)


