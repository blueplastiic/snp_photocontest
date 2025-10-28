from typing import Self
from functools import lru_cache

from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField

from models_app.models import User

from rest_framework.authtoken.models import Token

class UpdateTokenService(ServiceWithResult):
    user = ModelField(User)
    
    def process(self) -> Self: #pyright: ignore
        if self.is_valid():
            self.result = self.update_token()
        return self

    @property
    @lru_cache()
    def _user(self) -> User:
        return self.cleaned_data['user']

    def update_token(self) -> Token:
        Token.objects.get(user=self._user)
        return Token.objects.create(user=self._user)

