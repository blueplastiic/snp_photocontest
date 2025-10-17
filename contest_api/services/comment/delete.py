from typing import Self, Optional
from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from django import forms

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound, ValidationError
from service_objects.fields import ModelField

from models_app.models import Comment, User

class DeleteCommentService(ServiceWithResult):
    photo_id = forms.IntegerField()
    comment_id = forms.IntegerField()
    user = ModelField(User)

    custom_validations = [
        'comment_presence','comment_author_check', 
        'related_comments_presence'
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
    def _comment(self) -> Optional[Comment]:
        try:
            return (
                Comment.objects
                .prefetch_related('children')
                .get(id=self.cleaned_data['comment_id'])
            )
        except ObjectDoesNotExist:
            return None

    def delete_comment(self) -> None:
        self._comment.delete() #pyright: ignore 

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

    def related_comments_presence(self)-> None:
        if self._comment.children.exists():#pyright:ignore
            self.add_error(
                'comment_id',
                ValidationError(
                    message=f"Can't update comments with existing replies"
                )
            )


