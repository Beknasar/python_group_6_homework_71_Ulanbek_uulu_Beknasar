from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta


class Profile(models.Model):
    user: AbstractUser = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.ImageField(null=True, blank=True, upload_to='user_pics', verbose_name='Аватар')
    link = models.CharField(max_length=200, null=True, blank=True, verbose_name='Ссылка на профиль GitHub')
    about = models.TextField(max_length=2000, null=True, blank=True, verbose_name='О себе')

    def __str__(self):
        return self.user.get_full_name() + "'s Profile"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
