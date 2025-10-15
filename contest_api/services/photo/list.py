from .base_list import BaseListPhotoService
from utils.statuses import PhotoStatus

from models_app.models import Photo
from django.db.models import QuerySet


class ListPhotoService(BaseListPhotoService):
    
    @property
    def _filtered_photos(self) -> QuerySet[Photo]:
        photos =super()._filtered_photos
        return photos.filter(status=PhotoStatus.APPROVED)

