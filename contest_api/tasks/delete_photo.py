from django.core.exceptions import ObjectDoesNotExist

from utils.statuses import PhotoStatus

from models_app.models import Photo

from celery import shared_task


@shared_task(bind=True)
def delete_photo_task(photo_id: int) -> None:
    try:
        photo = Photo.objects.get(id=photo_id)
        if photo.status == PhotoStatus.DELETED:
            photo.delete()
    except ObjectDoesNotExist as exc: 
        pass
        #TODO: logging
    
