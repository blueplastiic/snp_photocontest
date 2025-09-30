from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import NotFound, ValidationError
from models_app.models import Photo, User, Vote
from django import forms

class CreateVoteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self): #pyright: ignore
        photo_id = self.cleaned_data.get('id')
        user = self.cleaned_data.get('user')

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            raise NotFound(additional_info='Photo does not exist')

        if Vote.objects.filter(user=user, photo=photo).exists():
            raise ValidationError(additional_info='You cannot vote twice')

        Vote.objects.create(photo=photo, user=user)

        return self
            
