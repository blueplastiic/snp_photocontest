from functools import lru_cache
from typing import Self

from utils.photo_order_fields import fields
from utils.statuses import PhotoStatus

from django.core.paginator import Page, EmptyPage, Paginator
from django.db.models import QuerySet, Count, Q
from django import forms
from django.conf import settings

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError

from models_app.models import Photo, User


class ListCurrentUserPhotoService(ServiceWithResult):
    user = ModelField(User)
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)

    order = forms.CharField(required=False)
    search_string = forms.CharField(required=False)
    status = forms.CharField(required=False)

    custom_validations = ['order_validation', 'status_validation']

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
    def _cur_user_photos(self) -> QuerySet[Photo]:
        return (
            Photo.objects
            .select_related('user')
            .annotate(
                num_comments=Count('comments'),
                num_votes=Count('votes')
                      )
            .filter(user=self._user)
        )

    @property
    def _filtered_photos(self) -> QuerySet[Photo]:
        photos =self._cur_user_photos
        search_string = self.cleaned_data.get('search_string')
        status = self.cleaned_data.get('status')

        if search_string:
            photos = photos.filter(
            Q(user__username__icontains=search_string) |
            Q(title__icontains=search_string) |
            Q(description__icontains=search_string)
            )

        if status:
            photos = photos.filter(status=status)
            
        return photos

    @property
    def _sorted_photos(self) -> QuerySet[Photo]:
        photos = self._filtered_photos
        order = self.cleaned_data.get('order')
        
        if order:
            return photos.order_by(order)
        else:
            return photos.order_by('-pub_date')

    @property
    def paginated_photos(self) -> Page:
        try:
            return Paginator(
                object_list=self._sorted_photos,
                per_page = self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(self.cleaned_data.get('page') or 1)
        except EmptyPage:
            return Paginator(
                object_list=Photo.objects.none(),
                per_page = self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(1)

    def order_validation(self):
        order = self.cleaned_data.get('order')

        if order:
            if order not in fields:
                self.add_error(
                    'order',
                    ValidationError(
                        message = 'Allowed params: pub_date, -pub_date, num_votes, -num_votes'
                    )
                )

    def status_validation(self):
        status = self.cleaned_data.get('status')
        allowed_statuses=PhotoStatus.STATUS_LIST
        
        if status: 
            if status not in allowed_statuses:
                self.add_error(
                    'status',
                    ValidationError(
                        message = f'Allowed params: {allowed_statuses}'
                    )
                )

