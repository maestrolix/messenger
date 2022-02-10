from rest_framework.exceptions import NotFound, ValidationError, PermissionDenied

from config.global_services import logic_exception_handler
from thread.models import *


@logic_exception_handler
def create_message(request) -> Message:
    """ Создание сообщения """
    data = request.data
    user = request.user
    try:
        thread_pk = data['thread_id']
        text = data['text']
    except KeyError as e:
        raise ValidationError(e)
    thread = Thread.objects.select_related('last_message').get(id=thread_pk)
    message = Message.objects.create(text=text, author=user, thread=thread)
    thread.last_message = message
    thread.save(update_fields=['last_message'])
    return message


@logic_exception_handler
def get_message(message_pk: int):
    """ Получение сообщения """
    try:
        return Message.objects.get(pk=message_pk)
    except Message.DoesNotExist as e:
        raise NotFound(e)


@logic_exception_handler
def delete_message_for_all(request) -> None:
    """ Безвозвратное удаление сообщения для всех """
    user = request.user
    try:
        message_ids = request.data['message_ids']
    except KeyError as e:
        raise ValidationError(e)
    messages_on_delete = Message.objects.filter(id__in=[*message_ids]).only('author_id')
    for message in messages_on_delete.all():
        if user.id != message.author_id:
            raise PermissionDenied()
    messages_on_delete.delete()


@logic_exception_handler
def update_message(request, message_pk) -> Thread:
    """ Обновление сообщения """
    user = request.user
    data = request.data
    try:
        text = data['text']
    except KeyError as e:
        raise ValidationError(e)
    message = Message.objects.select_related('author').get(id=message_pk)
    if user == message.author:
        message.text = text
        message.save(update_fields=['text'])
        return message
    raise PermissionDenied()


@logic_exception_handler
def delete_message_for_auth_user(request) -> None:
    """ Удаление сообщений в видимости аутентифицированного """
    try:
        message_ids = request.data['message_ids']
    except KeyError as e:
        raise ValidationError(e)
    try:
        request.user.user_deleted_messages.add(*message_ids)
    except Exception as e:
        raise NotFound('Не все id в списке присутствуют в сообщениях %s' % e)


@logic_exception_handler
def create_photo_of_message(request) -> None:
    """ Создание фотографий сообщения """
    user = request.user
    try:
        message_id = request.data['message_id']
        images = request.data['images']
    except KeyError as e:
        raise ValidationError(e)
    message = Message.objects.select_related('thread').get(id=message_id)
    message_photos = []
    for image in images:
        message_photo = MessagePhoto(
            image=image,
            thread=message.thread,
            message=message,
            sender=user
        )
        message_photos.append(message_photo)
    MessagePhoto.objects.bulk_create(message_photos)
