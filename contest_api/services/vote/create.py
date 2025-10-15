from typing import Optional, Self
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import NotFound, ValidationError

from models_app.models import Photo, User, Vote
from django import forms

class CreateVoteService(ServiceWithResult):
    photo_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = ['photo_presence', 'vote_dup']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.create_vote()
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

    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                "photo_id",
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

    def vote_dup(self) -> None:
        vote_exists = Vote.objects.filter(
            user=self._user,
            photo=self._photo
        ).exists()

        if vote_exists:
            self.add_error(
                "user",
                ValidationError(
                    message=f"User {self._user.id} has already voted for photo {self._photo.id}" #pyright: ignore
                )
            )

    def create_vote(self) -> None:
        Vote.objects.create(
            user=self.cleaned_data['user'],
            photo=self._photo
        )

