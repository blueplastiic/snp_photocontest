from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound

from models_app.models import Photo, User
from django import forms
from django.db.models import Count

class GetPhotoList(ServiceWithResult):
    user_id = forms.IntegerField(required=False)

    def process(self): #pyright: ignore
        user_id = self.cleaned_data.get('user_id')
        
        photos = None

        if user_id:
            try:        
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                raise NotFound(additional_info='User does not exist')
        
            photos = (
                Photo.objects
                .annotate(num_comments=Count('comments'))
                .annotate(num_votes=Count('votes'))
                .filter(user_id=user_id)
            )

        else:
            photos = Photo.objects.all()
        
        self.result = photos
        return self

