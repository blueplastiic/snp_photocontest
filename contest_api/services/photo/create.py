from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError
from service_objects.fields import ModelField
from models_app.models import Photo, User
from django import forms
from utils.statuses import PhotoStatus

class CreatePhotoService(ServiceWithResult):
    user = ModelField(User)
    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=300)
    photo = forms.ImageField()

    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')
        photo = self.cleaned_data.get('photo')

        if Photo.objects.filter(user=user, title=title).exists():
            raise ValidationError(additional_info='You already have a photo with this title')

        new_photo = Photo.objects.create(user=user,
                                         title=title,
                                         description=description,
                                         photo=photo,
                                         status=PhotoStatus.PENDING)
        
        return self

