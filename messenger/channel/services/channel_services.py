from channel.models import *

from rest_framework.exceptions import ValidationError
from channel.services.general_services import get_channel, get_user, permission

from config.global_services import logic_exception_handler


@logic_exception_handler
def get_channels(user) -> Channel:
    """ Получение каналов пользователя """
    return Channel.objects.filter(participants__in=[user])


@logic_exception_handler
def create_channel(request) -> Channel:
    """ Создание канала """
    try:
        title = request.data['title']
        description = request.data['description']
        avatar = request.data['avatar']
    except KeyError as e:
        raise ValidationError(f'{e} is required field')
    channel = Channel.objects.create(
        title=title,
        description=description,
        avatar=avatar,
        creator=request.user
    )
    channel.participants.add(request.user)
    return channel


@logic_exception_handler
def update_channel(channel_pk: int, request) -> Channel:
    """ Обновление информации о канале """
    channel = get_channel(channel_pk)
    if request.user == channel.creator:
        channel.title = request.data.get('title', channel.title)
        channel.avatar = request.data.get('avatar', channel.avatar)
        channel.description = request.data.get('description', channel.description)
        channel.save(update_fields=['title', 'avatar', 'description'])
    return channel


@logic_exception_handler
def delete_channel(channel_pk: int) -> None:
    """ Удаление канала """
    Channel.objects.get(id=channel_pk).delete()


# Это гавно надо будет переписать
@logic_exception_handler
def add_or_delete_user_from_channel(user, channel_pk: int) -> dict:
    """ Отписаться или подписаться на канал """
    channel = Channel.objects.prefetch_related('participants', 'black_list').get(id=channel_pk)
    subscribe = ''
    if user in channel.participants.all():
        channel.participants.remove(user)
        subscribe = False
    else:
        if user in channel.black_list.all():
            pass
        else:
            channel.participants.add(user)
            subscribe = True
    return {'channel': channel, 'subscribe': subscribe}


@logic_exception_handler
def delete_user_from_channel_by_admin(user_pk: int, admin, channel_pk: int) -> Channel:
    """ Удаление пользователя из канала администратором """
    channel = Channel.objects.prefetch_related('participants').get(id=channel_pk)
    user = get_user(user_pk)
    if permission(admin=admin, channel=channel):
        channel.participants.remove(user)
        channel.black_list.add(user)
    return channel


@logic_exception_handler
def get_params_for_add_delete_from_channel(request):
    """ Получение данных для добавления или удаления админа из канала """
    try:
        channel_pk = request.data['channel_pk']
        admin_pk = request.data['admin_pk']
    except KeyError as e:
        raise ValidationError(f'{e} is required field')
    channel = Channel.objects.select_related('creator').prefetch_related('admins').get(id=channel_pk)
    user = get_user(admin_pk)
    creator = request.user
    return channel, user, creator


@logic_exception_handler
def add_admin_in_channel_by_creator(request) -> Channel:
    """ Добавление админа в канал """
    channel, user, creator = get_params_for_add_delete_from_channel(request)
    if not (user in channel.admins.all()) and creator == channel.creator:
        channel.admins.add(user)
    return channel


@logic_exception_handler
def delete_admin_from_channel_by_creator(request) -> Channel:
    """ Удаления админа """
    channel, user, creator = get_params_for_add_delete_from_channel(request)
    if creator == channel.creator and user in channel.admins.all():
        channel.admins.remove(user)
    return channel
