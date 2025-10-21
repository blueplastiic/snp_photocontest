from typing import Self

from service_objects.services import ServiceWithResult
from service_objects.errors import ValidationError

from django import forms

from utils.password import validate_password
from models_app.models import User


class CreateUserService(ServiceWithResult):
    email = forms.EmailField()
    username = forms.CharField(max_length=20)
    password = forms.CharField(min_length=8, max_length=20)
    about = forms.CharField(max_length=500, required=False)

    custom_validations = ['email_presence', 'username_presence', 'password_validation']
    def process(self) -> Self: #pyright: ignore
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.create_user()
        return self

    def email_presence(self) -> None:
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            self.add_error(
                'email',
                ValidationError(
                    message=f"Email {self.cleaned_data['email']} is already registered"
                )
            )
    
    def username_presence(self) -> None:
        if User.objects.filter(username=self.cleaned_data['username'].exists()):
            self.add_error(
                'username',
                ValidationError(
                    message=f"Username {self.cleaned_data['username']} is already taken"
                )
            )

    def password_validation(self) -> None:
        if not validate_password(self.cleaned_data['password']):
            self.add_error(
                'password',
                ValidationError(
                    message=f"Password does not meet the requirements"
                )
            )

    def create_user(self) -> User:
        return User.objects.create(
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password'],
            about=self.cleaned_data['about']
        )

