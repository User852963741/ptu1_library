from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile',
        verbose_name='vartotojas',
    )
    picture = models.ImageField('nuotrauka', upload_to='user_profile/pictures', null=True, blank=True)

    def __str__(self):
        return str(self.user)
