from django.conf import settings
from django.db.models.signals import post_save 
from django.dispatch import receiver 
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import BaseUserManager, Group

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError('You must provide an email')
        if not username:
            raise ValueError('Yout must provide a username')
        if not password:
            raise ValueError('You must provide a password')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()

        if other_fields.get('is_staff') and not other_fields.get('is_superuser'):
            moderators_group,_=Group.objects.get_or_create(name='Moderators')
            user.groups.add(moderators_group)
        elif not (other_fields.get('is_staff') and other_fields.get('is_superuser')):
            participants_group,_=Group.objects.get_or_create(name='Participants')
            user.groups.add(participants_group)

        return user

    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('is_staff must be True for superuser')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True for superuser')

        return self.create_user(email, username, password, **other_fields)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

