from functools import lru_cache
from typing import Self

from django.db.models import QuerySet
from django.db.models import Count

from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import Photo, User

class ListCurrentUserPhotoService(ServiceWithResult):
    user = ModelField(User)

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.list_cur_user_photo()
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    def list_cur_user_photo(self) -> QuerySet:
        return (
            Photo.objects
            .annotate(
                num_comments=Count('comments'),
                num_votes=Count('votes')
                      )
            .filter(user=self._user)
        )

