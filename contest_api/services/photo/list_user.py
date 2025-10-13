from functools import lru_cache
from typing import Self, Optional
from utils.photo_order_fields import fields

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Count, Q
from django import forms
from django.core.paginator import Paginator, Page, EmptyPage
from django.conf import settings

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ValidationError

from models_app.models import Photo, User


class ListUserPhotoService(ServiceWithResult):
    user_id = forms.IntegerField()
    page=forms.IntegerField(required=False)
    per_page=forms.IntegerField(required=False)

    order = forms.CharField(required=False)
    search_string = forms.CharField(required=False)

    custom_validations = ['user_presence', 'order_validation']
    
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

    @property
    def _user_photos(self) -> QuerySet:
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
        photos =self._user_photos
        search_string = self.cleaned_data.get('search_string')

        if search_string:
            photos = photos.filter(
            Q(user__username__icontains=search_string) |
            Q(title__icontains=search_string) |
            Q(description__icontains=search_string)
            )

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
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
            ).page(self.cleaned_data.get('page') or 1)
        except EmptyPage:
            return Paginator(
                object_list=Photo.objects.none(),
                per_page=self.cleaned_data.get('per_page') or settings.REST_FRAMEWORK['PAGE_SIZE']
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

    def user_presence(self) -> None:
        if self.cleaned_data.get('user_id'):
            if not self._user:
                self.add_error(
                    'user_id',
                    NotFound(
                        message=f"User {self.cleaned_data['user_id']} not found"
                    )
                )


