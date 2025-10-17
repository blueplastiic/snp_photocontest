from typing import Self, Optional
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Prefetch
from django import forms

from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import Comment, Photo


class ListCommentService(ServiceWithResult):
    photo_id=forms.IntegerField()
    custom_validations = ['photo_presence']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._comments
        return self

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        try:
            return (
                Photo.objects
                .get(id=self.cleaned_data['photo_id'])
                    )
        except ObjectDoesNotExist:
            return None
   
    @property
    def _comments(self) -> QuerySet[Comment]:
        return (
            Comment.objects
            .prefetch_related('user', Prefetch('children__user'))
            .filter(photo=self._photo)
        )

    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                'photo_id',
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

