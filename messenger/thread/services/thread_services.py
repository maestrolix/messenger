from thread.models import *
from config.global_services import logic_exception_handler

from rest_framework.exceptions import NotFound, ValidationError

from django.db.models import Q


@logic_exception_handler
def get_thread_without_delete_messages(request, thread_pk: int):
    """ Получение диалога """
    user = request.user
    thread = Thread.objects.prefetch_related('thread_messages__message_photos').exclude(
        thread_messages__who_deleted_the_message__in=[user]).get(id=thread_pk)
    return thread


@logic_exception_handler
def thread_create(request) -> Thread:
    """ Создание диалога """
    try:
        participants = request.data['participants']
    except KeyError as e:
        raise ValidationError(e)
    new_thread = Thread.objects.create()
    new_thread.participants.set(participants)
    return new_thread


@logic_exception_handler
def active_threads_list(request) -> Thread:
    """ Получение активных диалогов """
    user = request.user
    threads = Thread.objects.select_related('last_message', 'last_message__author').filter(
        participants__in=[user]).exclude(
        Q(archive__in=[user]) |
        Q(deleted__in=[user]
          )
    )
    return threads


@logic_exception_handler
def archive_threads_list(request) -> Thread:
    """ Получение диалогов в архивах """
    user = request.user
    threads = Thread.objects.select_related('last_message', 'last_message__author').filter(
        Q(participants__in=[user]) &
        Q(archive__in=[user])
    ).exclude(deleted__in=[user])
    return threads


@logic_exception_handler
def edit_push_notification_thread(thread_pk: int, request) -> Thread:
    """ Настройка пользовательских уведомлений """
    thread = Thread.objects.get(pk=thread_pk)
    user = request.user
    if user in thread.push_notification.all():
        thread.push_notification.remove(user)
    else:
        thread.push_notification.add(user)
    return thread.push_notification


@logic_exception_handler
def delete_thread_for_auth_user(request, thread_pk: int) -> None:
    """ Удаления диалога в видимости аутентифицированного пользователя """
    thread = Thread.objects.get(id=thread_pk)
    message_ids_to_delete_for_user = list(thread.thread_messages.values_list('id', flat=True))
    request.user.user_deleted_messages.add(*message_ids_to_delete_for_user)


# Переписать это тоже
@logic_exception_handler
def add_or_delete_from_archive_thread(request, thread_pk: int) -> Thread:
    """ Добавление или очистка из архивных диалогов """
    user = request.user
    thread = Thread.objects.get(id=thread_pk)
    if user in thread.archive.all():
        thread.archive.remove(user)
        active_threads = Thread.objects.select_related('last_message', 'last_message__author').filter(
            participants__in=[user]).exclude(
            archive__in=[user]).all()
        return active_threads
    else:
        thread.archive.add(user)
        archive_threads = user.archive_threads.select_related('last_message', 'last_message__author').all()
        return archive_threads
