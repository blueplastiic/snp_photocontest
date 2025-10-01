from service_objects.services import ServiceWithResult
from service_objects.errors import NotFound
from service_objects.fields import ModelField
from django import forms
from models_app.models import Photo, User, Comment

class CreateCommmentService(ServiceWithResult):
    user = ModelField(User)
    id = forms.IntegerField()
    content = forms.CharField()

    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        photo_id = self.cleaned_data.get('id')
        content = self.cleaned_data.get('content')

        try:
            photo = Photo.objects.get(id=photo_id)
        except Photo.DoesNotExist:
            raise NotFound(additional_info='Photo does not exist')

        comment = Comment.objects.create(
            content = content,
            user = user,
            photo = photo
        )

        return self

