from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError
from django import forms
from utils.password import validate_password
from models_app.models import User

class RegisterUserService(ServiceWithResult):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=8, max_length=20)
    about = forms.CharField(max_length=500, required=False)

    def process(self): #pyright: ignore
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        about = self.cleaned_data.get('about')

        if User.objects.filter(username=username).exists():
            raise ValidationError(additional_info='This username is already taken')

        if User.objects.filter(email=email).exists():
            raise ValidationError(additional_info='This email is already registered')

        if not validate_password(password):
            raise ValidationError(additional_info="Password doesn't meet the requirements")

        new_user = User.objects.create_user(email=email, username=username, password=password, about=about) #pyright: ignore

        self.result = new_user
        return self

