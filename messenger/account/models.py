from django.db import models
from django.contrib.auth.models import AbstractUser
from config.global_services import get_upload_path


class AdvUser(AbstractUser):
    is_online = models.BooleanField(default=False, verbose_name="Онлайн")
    last_active = models.DateTimeField(auto_now_add=True, verbose_name="Последнее посещение сайта")
    telephone = models.CharField(max_length=12, null=True, verbose_name="Телефон")
    about_user = models.TextField(max_length=100, null=True, verbose_name='Информация о пользователе', unique=True)
    is_verified = models.BooleanField(default=False, verbose_name="Подтверждён ли пользователь через почту")
    key = models.BigIntegerField(null=True, db_index=True, verbose_name="Ключ для подтверждения почты")

    class Meta(AbstractUser.Meta):
        db_table = 'user'


class AvatarImageProfile(models.Model):
    image = models.ImageField(upload_to=get_upload_path('images/account/avatars/'),
                              verbose_name='Фотография пользователя'
                              )
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='profile_avatars')

    class Meta:
        db_table = 'avatar_image_profile'
        verbose_name_plural = 'Фотография пользователя'
        verbose_name = 'Фотографии пользователей'
