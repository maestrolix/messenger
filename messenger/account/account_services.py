import random

from account.models import AdvUser, AvatarImageProfile
from config.global_services import logic_exception_handler
from config.settings import EMAIL_HOST_USER

from rest_framework.exceptions import NotFound, ValidationError

from django.core.mail import send_mail
from django.urls import reverse


def registration_user(request):
    """ Регистрация пользователя """
    data = request.data
    try:
        username = data['username']
        if AdvUser.objects.filter(username=username).only('id').first() is None:
            try:
                password = data['password']
                email = data['email']
            except KeyError as e:
                raise ValidationError(f"Invalid {e}")
            # Создаём ключ подтверждения аккаунта
            key = random.randint(10000000000000000, 90000000000000000)
            user_keys = list(AdvUser.objects.values_list('key', flat=True))
            while key in user_keys:
                key = random.randint(10000000000000000, 90000000000000000)
            new_user = AdvUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                is_verified=False,
                key=key
            )
            html_message = f"<a href='http://" \
                           f"{request.get_host() + reverse('account:confirm_account', kwargs={'key': key})}'>" \
                           f"Перейдите по данной ссылке, чтобы подтвердить ваш аккаунт</a>"
            send_mail('Hello', None, EMAIL_HOST_USER, [email],
                      fail_silently=True, html_message=html_message)
            return new_user
        else:
            raise ValidationError('Пользователь с ником %s уже существует' % username)
    except KeyError as e:
        raise ValidationError(f'Invalid {e}')


@logic_exception_handler
def update_user(request) -> AdvUser:
    """ Обновление информации о пользователе """
    user = request.user
    user.username = request.data.get('username', user.username)
    user.first_name = request.data.get('first_name', user.first_name)
    user.last_name = request.data.get('last_name', user.last_name)
    user.about_user = request.data.get('about_user', user.about_user)
    user.telephone = request.data.get('telephone', user.telephone)
    user.save(update_fields=['username', 'first_name', 'last_name', 'about_user', 'telephone'])
    return user


def get_profile_of_user(user_id: int) -> dict:
    """ Получение информации о пользователе """
    try:
        return AdvUser.objects.get(id=user_id)
    except AdvUser.DoesNotExist as e:
        raise NotFound(e)


@logic_exception_handler
def create_photo_user(data, user) -> None:
    """ Создание нового аватара пользователя """
    try:
        image = data['image']
    except KeyError as e:
        raise ValidationError(e)
    AvatarImageProfile.objects.create(
        image=image,
        user=user
    )


def delete_photo_user(photo_pk) -> None:
    """ Удаление аватара пользователя """
    try:
        AvatarImageProfile.objects.get(id=photo_pk).delete()
    except AvatarImageProfile.DoesNotExist as e:
        raise NotFound(e)
