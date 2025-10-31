from datetime import timedelta
from functools import lru_cache
from typing import Optional, Self

from contest_api.tasks.delete_photo import delete_photo_task

from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django import forms

from service_objects.errors import NotFound
from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from models_app.models import User, Photo, Comment
from utils.statuses import PhotoStatus

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from utils.notification import build_notification

class DeletePhotoService(ServiceWithResult):
    user = ModelField(User)
    photo_id = forms.IntegerField()

    custom_validations = ['photo_presence', 'status_check']

    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.delete_photo()
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    @property
    @lru_cache()
    def _photo(self) -> Optional[Photo]:
        try:
            return (
                Photo.objects
                .get(id= self.cleaned_data['photo_id'], user=self._user)
            )

        except ObjectDoesNotExist:
            return None

    def delete_photo(self) -> None:
        photo = self._photo
        if photo.status in (PhotoStatus.REJECTED, PhotoStatus.PENDING): #pyright:ignore
            photo.delete() #pyright:ignore

            channel_layer = get_channel_layer()
            photo_comments = Comment.objects.filter(photo=self._photo)

            for comment in photo_comments:
                async_to_sync(channel_layer.group_send)(
                    str(comment.user_id),
                    build_notification(
                        type='send_notification',
                        action='delete_photo',
                        photo_id=self.cleaned_data['photo_id'],
                        initiator_username=self._user.username,
                    )
                )

            return

        photo.status = PhotoStatus.DELETED #pyright:ignore
        photo.save() #pyright: ignore

        execute_time = timezone.now() + timedelta(minutes=1) #days=1
        delete_photo_task.apply_async(  #pyright: ignore
            args=[self.cleaned_data['photo_id']],
            eta=execute_time
        )

    def photo_presence(self) -> None:
        if not self._photo:
            self.add_error(
                'photo_id',
                NotFound(
                    message=f"Photo {self.cleaned_data['photo_id']} not found"
                )
            )

    def status_check(self) -> None:
        if self._photo.status == PhotoStatus.DELETED: #pyright:ignore
            self.add_error(
                'photo_id',
                ValidationError(
                    message=f"Photo {self.cleaned_data['photo_id']} deletion is already scheduled"
                )
            )

