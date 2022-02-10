from django.db import models

from config.global_services import get_upload_path
from account.models import AdvUser


class Thread(models.Model):
    """ Диалоги месенжера """

    push_notification = models.ManyToManyField(AdvUser, related_name='push_notification_threads',
                                               verbose_name='Пользователи с уведомлениями')
    archive = models.ManyToManyField(AdvUser, related_name='archive_threads',
                                     verbose_name='Пользователи архивировавшие диалог')
    participants = models.ManyToManyField(AdvUser, related_name='user_threads', verbose_name='Участники диалога')
    deleted = models.ManyToManyField(AdvUser, related_name='deleted_threads',
                                     verbose_name='Пользователи удалившие диалог')

    last_message = models.ForeignKey('Message', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='last_message_of_thread',
                                     verbose_name='Последнее сообщение диалога')

    def __str__(self):
        string = ''
        for participant in self.participants.values('first_name'):
            string += '%s ' % participant['first_name']
        return string

    class Meta:
        db_table = 'thread'
        verbose_name_plural = 'Диалог'
        verbose_name = 'Диалоги'


class Message(models.Model):
    """ Сообщения диалога """

    text = models.TextField(max_length=10000, verbose_name='Текст сообщения')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='user_messages',
                               verbose_name='Создатель сообщения')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_messages')
    created_at = models.DateTimeField(auto_now_add=True)
    who_deleted_the_message = models.ManyToManyField(AdvUser, related_name='user_deleted_messages',
                                                     verbose_name='Пользователи удалившие сообщение')

    class Meta:
        db_table = 'message'
        verbose_name_plural = 'Сообщение'
        verbose_name = 'Сообщения'


class MessagePhoto(models.Model):
    """ Фотографии, которые прикрепляют к сообщению """

    image = models.ImageField(upload_to=get_upload_path('thread/messages/'), verbose_name='Фотография сообщения')
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='thread_messages_photos',
                               verbose_name='Диалог фотографии')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message_photos',
                                verbose_name='Сообщение фотографии')
    sender = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='user_message_photos',
                               verbose_name='Отправитель фотографии')

    class Meta:
        db_table = 'message_photo'
        verbose_name_plural = 'Фотография сообщения'
        verbose_name = 'Фотографии сообщений'
