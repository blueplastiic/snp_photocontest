from typing import Self
from utils import order_choices

from django.core.paginator import Paginator, Page, EmptyPage
from django.db.models import QuerySet, Count, Q
from django import forms
from django.conf import settings

from service_objects.services import ServiceWithResult

from models_app.models import Photo


class BaseListPhotoService(ServiceWithResult):
    per_page = forms.IntegerField(required=False)
    page = forms.IntegerField(required=False)

    order = forms.ChoiceField(choices=order_choices.ORDER_CHOICES, required=False)
    search = forms.CharField(required=False)

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
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
        )

    @property
    def _filtered_photos(self) -> QuerySet[Photo]:
        photos =self._photos
        search = self.cleaned_data.get('search')

        if search:
            photos = photos.filter(
            Q(user__username__icontains=search) |
            Q(title__icontains=search) |
            Q(description__icontains=search)
            )

        return photos

    @property
    def _sorted_photos(self) -> QuerySet[Photo]:
        photos = self._filtered_photos
        order = self.cleaned_data.get('order')
        
        if order:
            return photos.order_by(order)
        return photos.order_by('-pub_date')

    @property
    def _paginated_photos(self) -> Page:
        try:
            return Paginator(
                object_list=self._sorted_photos,
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(self.cleaned_data.get('page') or 1)
        except EmptyPage:
            return Paginator(
                object_list=Photo.objects.none(),
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(1)

