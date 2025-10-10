from functools import lru_cache
from typing import Self

from django.core.paginator import Page, EmptyPage, Paginator
from django.db.models import QuerySet
from django.db.models import Count
from django import forms
from django.conf import settings

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Photo, User

class ListCurrentUserPhotoService(ServiceWithResult):
    user = ModelField(User)
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.paginated_photos
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    @property
    def cur_user_photos(self) -> QuerySet[Photo]:
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
                object_list=self.cur_user_photos,
                per_page = self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(self.cleaned_data.get('page') or 1)
        except EmptyPage:
            return Paginator(
                object_list=Photo.objects.none(),
                per_page = self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(1)

