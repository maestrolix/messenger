from config.global_services import logic_exception_handler

from channel.models import Post, Channel, ImagePost
from channel.services.general_services import permission, get_channel, get_post

from rest_framework.exceptions import ValidationError


@logic_exception_handler
def create_post(request, channel_pk) -> Channel:
    """ Создание публикации """
    try:
        text = request.data['text']
        channel = get_channel(channel_pk=channel_pk)
        if permission(admin=request.user, channel=channel):
            Post.objects.create(
                text=text,
                channel=channel
            )
            return channel
    except KeyError as e:
        raise ValidationError(f'{e} is required field')


@logic_exception_handler
def update_post(request, post_pk: int) -> Channel:
    """ Обновление публикации """
    try:
        text = request.data['text']
    except KeyError as e:
        raise ValidationError(f'{e} is required field')
    post = Post.objects.select_related('channel').get(id=post_pk)
    if permission(admin=request.user, channel=post.channel):
        post.text = text
        post.save(update_fields=['text'])
    return post


@logic_exception_handler
def delete_post(post_pk: int, admin) -> Channel:
    """ Удаление публикации """
    post = Post.objects.select_related('channel', 'channel__creator').prefetch_related('channel__posts').get(
        id=post_pk)
    channel = post.channel
    if permission(admin=admin, channel=channel):
        post.delete()
    return channel


@logic_exception_handler
def create_image_post(request) -> Channel:
    """ Создание фотографии публикации """
    try:
        post_pk = request.data['post_pk']
        image = request.data['image']
    except KeyError as e:
        raise ValidationError(f'{e} is required field')
    post = get_post(post_pk)
    if permission(admin=request.user, channel=post.channel):
        ImagePost.objects.create(
            image=image,
            post=post,
            channel=post.channel,
            sender=request.user
        )
    return post.channel
