from typing import Self, Optional
from functools import lru_cache

from service_objects.errors import NotFound, ValidationError
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models import User, Comment

class UpdateCommentService(ServiceWithResult):
    user = ModelField(User)
    comment_id = forms.IntegerField()
    content = forms.CharField()

    custom_validations = ['comment_presence','related_comments_presence']

    def process(self) -> Self: #pyright:ignore
        self.run_custom_validations()
        if self.is_valid():
            self.update_comment()
        return self

    @property
    @lru_cache()
    def _user(self) -> None:
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

    def update_comment(self)->None:
        comment = self._comment
        comment.content = self.cleaned_data['content'] #pyright: ignore
        comment.save() #pyright: ignore

    def comment_presence(self) -> None:
        if not self._comment:
            self.add_error(
                'comment_id',
                NotFound(
                    message=f"Comment {self.cleaned_data['comment_id']} does not exist"
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

