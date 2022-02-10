from config.global_services import logic_exception_handler

from channel.models import Comment, Channel
from channel.services.general_services import get_post

from rest_framework.exceptions import ValidationError, NotFound


@logic_exception_handler
def create_comment(request) -> Channel:
    """ Создание комментария """
    try:
        post_pk = request.data['post_pk']
        text = request.data['text']
    except KeyError as e:
        raise ValidationError(f'{e} is required field')
    post = get_post(post_pk)
    Comment.objects.create(
        author=request.user,
        text=text,
        post=post
    )
    return post.channel


def get_comment(comment_pk: int):
    """ Получение комментария """
    try:
        return Comment.objects.select_related('author', 'post__channel', 'post__channel__creator').get(
            pk=comment_pk)
    except Comment.DoesNotExist as e:
        raise NotFound(e)


@logic_exception_handler
def update_comment(request, comment_pk: int) -> Channel:
    """ Обновление комментария """
    try:
        text = request.data['text']
    except KeyError as e:
        raise ValidationError({'Error': f'{e} is required field'})
    comment = get_comment(comment_pk)
    if request.user == comment.author:
        comment.text = text
        comment.save(update_fields=['text'])
    return comment.post.channel


@logic_exception_handler
def delete_comment(comment_pk: int, user) -> Channel:
    """ Удаление комментария """
    comment = get_comment(comment_pk)
    channel = comment.post.channel
    if user == comment.author:
        comment.delete()
    return channel
