from thread.serializers import (ThreadListSerializer,
                                ThreadDetailSerializer,
                                MessageSerializer,
                                )
from account.serializers import AdvUserListSerializer

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from thread.services.thread_services import *
from thread.services.messenger_services import *


class ThreadList(APIView):
    """ Просмотр и создание активных диалогов пользователя """

    def get(self, request):
        threads = None
        if request.GET.get('type') == 'active':
            threads = active_threads_list(request=request)
        elif request.GET.get('type') == 'archive':
            threads = archive_threads_list(request=request)
        serializer = ThreadListSerializer(threads, many=True)
        return Response({'threads': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        thread = thread_create(request=request)
        serializer = ThreadDetailSerializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ThreadDetail(APIView):
    """ Детальная информация о диалоге """

    def get(self, request, thread_pk):
        thread = get_thread_without_delete_messages(request=request, thread_pk=thread_pk)
        data = ThreadDetailSerializer(thread).data
        return Response(data, status=status.HTTP_200_OK)


class EditPushThread(APIView):
    """ Редактирование уведомлений в диалоге """

    def put(self, request, thread_pk):
        response = edit_push_notification_thread(thread_pk=thread_pk, request=request)
        serializer = AdvUserListSerializer(response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EditDeletedThread(APIView):
    """ Удаление диалога для аутентифицированного пользователя только на его странице """

    def delete(self, request, thread_pk):
        delete_thread_for_auth_user(request=request, thread_pk=thread_pk)
        return Response('This dialog is not available to you', status=status.HTTP_204_NO_CONTENT)


class EditArchiveThread(APIView):
    """ Добавление диалога в архивы или наоборот """

    def put(self, request, thread_pk):
        response = add_or_delete_from_archive_thread(request=request, thread_pk=thread_pk)
        serializer = ThreadListSerializer(response, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageList(APIView):
    """ Публикация сообщения """

    def post(self, request):
        response = create_message(request=request)
        serializer = MessageSerializer(response)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        delete_message_for_all(request=request)
        return Response('Messages deleted!', status=status.HTTP_204_NO_CONTENT)

    def put(self, request):
        delete_message_for_auth_user(request=request)
        return Response('Messages deleted!', status=status.HTTP_204_NO_CONTENT)


class MessageDetail(APIView):
    """ Редактирование сообщения для всех """

    def put(self, request, message_pk):
        response = update_message(message_pk=message_pk, request=request)
        serializer = MessageSerializer(response)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessagePhotoList(APIView):
    """ Публикация фотографий прикреплённых к сообщению """

    def post(self, request):
        create_photo_of_message(request)
        return Response(status=status.HTTP_201_CREATED)
