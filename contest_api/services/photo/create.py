from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from models_app import Photo
from django import forms
from django.conf import settings
from utils.statuses import PhotoStatus

class CreatePhotoService(ServiceWithResult):
    User = settings.AUTH_USER_MODEL
    user = ModelField(User)
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)
    photo = forms.ImageField()

    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        photo = self.cleaned_data.get('photo')

        new_photo = Photo.objects.create(user=user,
                                         title=title,
                                         description=description,
                                         status=PhotoStatus.PENDING)
        
        return self

