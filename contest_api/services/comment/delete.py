from typing import Self, Optional
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from django import forms

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField

from models_app.models import Comment, User, Photo

class DeleteCommentService(ServiceWithResult):
    photo_id = forms.IntegerField()
    comment_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = [
        'photo_presence, comment_presence',
        'comment_author_check', 'comment_photo_check'
                          ]
    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.delete_comment()
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
    def _comment(self) -> Optional[Comment]:
        try:
            return Comment.objects.get(
                id=self.cleaned_data['comment_id']
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

    def comment_presence(self) -> None:
        if not self._comment:
            self.add_error(
                'comment_id',
                NotFound(
                    message=f"Comment {self.cleaned_data['comment_id']} not found"
                )
            )
    
    def comment_author_check(self) -> None:
        if self._comment.user_id != self._user.id: #pyright: ignore
            self.add_error(
                'user',
                ValidationError(
                    message="You can only delete your own comments"
                )
            )

    def comment_photo_check(self) -> None:
        if self._comment.photo_id != self._photo.id: #pyright: ignore
            self.add_error(
                'photo_id',
                ValidationError(
                    message=f"Comment {self._comment.id} does not belong to photo {self._photo.id}" #pyright:ignore
                )
            )

    def delete_comment(self) -> None:
        self._comment.delete() #pyright: ignore

