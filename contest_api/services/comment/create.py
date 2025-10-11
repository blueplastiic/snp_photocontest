from typing import Self, Optional
from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField

from models_app.models import Photo, User, Comment

class CreateCommmentService(ServiceWithResult):
    user = ModelField(User)
    photo_id = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    content = forms.CharField()

    custom_validations = ['photo_presence', 'comment_presence', 'comment_parent_presence']

    def process(self) -> Self:  #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.create_comment()
        
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
    def _parent(self) -> Optional[Comment]:
        try:
            return Comment.objects.get(
                id=self.cleaned_data['parent_id']
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

    def comment_presence(self) -> None:
        if self.cleaned_data.get('parent_id'): #checks only if client passed the id
            if not self._parent:
                self.add_error(
                    "parent_id",
                    NotFound(
                        message=f"Comment {self.cleaned_data['parent_id']} not found"
                    )
                )

    def comment_parent_presence(self) -> None:
        if self.cleaned_data.get('parent_id'):
            if self._parent.parent: #pyright: ignore
                self.add_error(
                    'parent_id',
                    forms.ValidationError(
                        message=f"Can't reply to replies"
                    )
                )

    def create_comment(self) -> None:
        Comment.objects.create(
            user=self._user,
            photo=self._photo,
            parent=self._parent,
            content=self.cleaned_data.get('content')
        )

