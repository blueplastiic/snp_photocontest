from django.core.exceptions import ObjectDoesNotExist

from utils.statuses import PhotoStatus

from models_app.models import Photo, Comment

from celery import shared_task

import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from utils.notification import build_notification

logger = logging.getLogger('celery')

@shared_task(bind=True)
def delete_photo_task(self, photo_id: int) -> None:
    try:
        photo = Photo.objects.get(id=photo_id)
        if photo.status == PhotoStatus.DELETED:
            photo.delete()

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
            logger.info(f"Task {self.request.id} has executed: photo {photo_id} is deleted")
    except ObjectDoesNotExist as exc: 
        logger.warning(f"Couldn't complete task {self.request.id}: photo {photo_id} not found")
    
