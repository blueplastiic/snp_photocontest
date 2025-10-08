from typing import Self, Optional
from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult

from models_app.models import Photo

class RetrievePhotoService(ServiceWithResult):
    photo_id = forms.IntegerField()

    custom_validations=['photo_presence']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._photo
        return self

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        try:
            return (Photo.objects
                    .annotate(num_votes=Count('votes'))
                    .get(id= self.cleaned_data['photo_id'])
                    )

        except ObjectDoesNotExist:
            return None
    
    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                'photo_id',
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

