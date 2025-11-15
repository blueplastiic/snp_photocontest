from typing import Self, Optional
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import NotFound

from models_app.models import Vote, Photo, User
from django import forms


class DeleteVoteService(ServiceWithResult):
    photo_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['photo_presence', 'vote_presence']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.delete_vote()
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        try:
            return Photo.objects.get(
                id=self.cleaned_data['photo_id']
            )
        except ObjectDoesNotExist:
            return None

    @property
    @lru_cache()
    def _vote(self) -> Optional[Vote]:
        try:
            return Vote.objects.get(
                photo = self._photo,
                user = self._user
            )
        except ObjectDoesNotExist:
            return None

    def delete_vote(self) -> None:
        self._vote.delete() #pyright: ignore
        
    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                "photo_id",
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

    def vote_presence(self) -> None:
        if not self._vote:
            self.add_error(
                "photo_id",
                NotFound(
                    message=f"Vote from user {self._user.id} for photo {self._photo.id} not found" #pyright: ignore
                )
            )

