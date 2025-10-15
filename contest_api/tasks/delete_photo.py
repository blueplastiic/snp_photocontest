from utils.statuses import PhotoStatus

from models_app.models import Photo

from celery import shared_task


@shared_task
def delete_photo_task(photo_id: int) -> None:
    photo = Photo.objects.get(id=photo_id)

    #user has time to cancel the deletion 
    #which is basically returning status to 'approved'
    #if not, then we BALL:
    if photo.status == PhotoStatus.DELETED:
        photo.delete()
    
