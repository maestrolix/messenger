from config.global_services import logic_exception_handler

from account.models import AdvUser
from channel.models import Channel, Post

from rest_framework.exceptions import NotFound, PermissionDenied


def get_user(user_pk):
    """ Получить пользователя """
    try:
        return AdvUser.objects.get(pk=user_pk)
    except AdvUser.DoesNotExist as e:
        raise NotFound(e)


@logic_exception_handler
def permission(admin, channel) -> bool:
    """ Проверка пользователя """
    if (admin.id == channel.creator_id) | (admin in channel.admins.all()):
        return True
    else:
        raise PermissionDenied


def get_channel(channel_pk: int) -> Channel:
    """ Проверка канала """
    try:
        return Channel.objects.select_related('creator').get(pk=channel_pk)
    except Channel.DoesNotExist as e:
        raise NotFound(e)


def get_post(post_pk) -> Post:
    """ Получение публикации """
    try:
        return Post.objects.select_related('channel', 'channel__creator').prefetch_related('channel__posts').get(
            id=post_pk)
    except Post.DoesNotExist as e:
        raise NotFound(e)
