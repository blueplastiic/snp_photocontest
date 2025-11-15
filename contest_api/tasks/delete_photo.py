from django.core.exceptions import ObjectDoesNotExist

from utils.statuses import PhotoStatus

from models_app.models import Photo

from celery import shared_task

import logging


logger = logging.getLogger('celery')

@shared_task(bind=True)
def delete_photo_task(self, photo_id: int) -> None:
    try:
        photo = Photo.objects.get(id=photo_id)
        if photo.status == PhotoStatus.DELETED:
            photo.delete()
            logger.info(f"Task {self.request.id} has executed: photo {photo_id} is deleted")
    except ObjectDoesNotExist as exc: 
        logger.warning(f"Couldn't complete task {self.request.id}: photo {photo_id} not found")
    
