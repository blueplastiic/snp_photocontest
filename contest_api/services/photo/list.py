from typing import Self

from django.db.models import QuerySet
from django.db.models import Count

from service_objects.services import ServiceWithResult

from models_app.models import Photo

class ListPhotoService(ServiceWithResult):
    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.list_photo()
        return self

    def list_photo(self) -> QuerySet:
        return (
            Photo.objects
            .annotate(
                num_comments=Count('comments'),
                num_votes=Count('votes')
                      )
        )

