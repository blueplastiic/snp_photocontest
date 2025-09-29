from service_objects.errors import NotFound
from service_objects.services import ServiceWithResult
from django import forms
from models_app.models import Photo
from django.db.models import Count

class GetPhotoByIdService(ServiceWithResult):
    id = forms.IntegerField()

    def process(self): #pyright: ignore
        id = self.cleaned_data.get('id')

        try:
            photo = (
                Photo.objects
                     .select_related('user')
                     .prefetch_related('comments')
                     .annotate(num_votes=Count('votes'))
                     .get(id=id)
            )
        except Photo.DoesNotExist:
            raise NotFound(additional_info='Photo does not exist')

        self.result = photo
        return self

