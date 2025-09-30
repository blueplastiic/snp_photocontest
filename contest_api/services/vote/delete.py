from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import NotFound
from models_app.models import Vote, Photo, User
from django import forms

class DeleteVoteService(ServiceWithResult):
    id = forms.IntegerField()
    user = ModelField(User)

    def process(self): #pyright: ignore
        photo_id = self.cleaned_data.get('photo_id')
        user = self.cleaned_data.get('user')

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            raise NotFound(additional_info='Photo does not exist')

        try:
            vote = Vote.objects.get(photo=photo, user=user)
        except Vote.DoesNotExist:
            raise NotFound(additional_info="You haven't voted yet")

        vote.delete()
        return self

