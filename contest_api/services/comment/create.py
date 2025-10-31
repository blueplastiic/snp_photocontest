from typing import Self, Optional
from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField

from models_app.models import Photo, User, Comment

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from utils.notification import build_notification

class CreateCommmentService(ServiceWithResult):
    user = ModelField(User)
    photo_id = forms.IntegerField()
    parent_id = forms.IntegerField(required=False)
    content = forms.CharField()

    custom_validations = ['photo_presence', 'comment_presence', 'comment_parent_presence']

    def process(self) -> Self:  #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.create_comment()
        
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

    def create_comment(self) -> Comment:
        comment = Comment.objects.create(
            user=self._user,
            photo=self._photo,
            parent=self._parent,
            content=self.cleaned_data.get('content')
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            str(self._photo.user_id),
            build_notification(
                type='send_notification',
                action='create_comment',
                photo_id=self.cleaned_data['photo_id'],
                initiator_username=self._user.username,
                votes_count=self._photo.comments.count()
            )
        )

        return comment


    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                "photo_id",
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

    def comment_presence(self) -> None:
        if self.cleaned_data.get('parent_id') and not self._parent: 
            self.add_error(
                "parent_id",
                NotFound(
                    message=f"Comment {self.cleaned_data['parent_id']} not found"
                )
            )

    def comment_parent_presence(self) -> None:
        if self.cleaned_data.get('parent_id') and self._parent.parent: #pyright:ignore
            self.add_error( #pyright:ignore
                'parent_id',
                forms.ValidationError(
                    message=f"Can't reply to replies"
                )
            )

