from django import forms
from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from service_objects.errors import ValidationError
from django.conf import settings

class UpdatePublicInfoService(ServiceWithResult):
    User = settings.AUTH_USER_MODEL
    user = ModelField(User)
    username = forms.CharField(max_length=30, required=False)
    about = forms.CharField(max_length=500, required=False)

    def process(self): #pyright: ignore
        user = self.cleaned_data.get('user')

        username = self.cleaned_data.get('username')
        about = self.cleaned_data.get('about')

        if not username and not about: 
            raise ValidationError('Data not provided')

        if username:
            if User.objects.filter(username=username).exclude(id=user.id).exists(): #pyright: ignore
                raise ValidationError('This username is already taken')
            user.username = username #pyright: ignore
        if about:
            user.about = about #pyright:ignore

        user.save() #pyright:ignore
        self.result = user
        return self

