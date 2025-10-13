from typing import Self

from django.core.paginator import Paginator, Page, EmptyPage
from django.db.models import QuerySet
from django.db.models import Count
from django import forms

from django.conf import settings

from service_objects.services import ServiceWithResult

from models_app.models import Photo


class ListPhotoService(ServiceWithResult):
    per_page = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)

    def process(self) -> Self: #pyright: ignore
        if self.is_valid():
            self.result = self._paginated_photos
        return self
   
    @property
    def _photos(self) -> QuerySet[Photo]:
        return (
            Photo.objects
            .select_related('user')
            .annotate(
                num_comments=Count('comments'),
                num_votes=Count('votes')
                      )
            .filter(status='A')
        )

    @property
    def _paginated_photos(self) -> Page:
        try:
            return Paginator(
                object_list=self._photos,
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(self.cleaned_data.get('page') or 1)
        except EmptyPage:
            return Paginator(
                object_list=Photo.objects.none(),
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(1)

