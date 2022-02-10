from channel.services.channel_services import *
from channel.services.post_services import *
from channel.services.comment_services import *
from channel.serializers import (ChannelListSerializer,
                                 PostSerializer,
                                 )
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response


def get_serializer_data(channel):
    return ChannelListSerializer(channel).data


class ChannelList(APIView):
    """ Список каналов пользователя и создание нового канала"""

    def get(self, request):
        channels = get_channels(user=request.user)
        data = ChannelListSerializer(channels, many=True).data
        return Response({'channels': data}, status=status.HTTP_200_OK)

    def post(self, request):
        new_channel = create_channel(request=request)
        return Response(get_serializer_data(new_channel), status=status.HTTP_201_CREATED)


class ChannelDetail(APIView):
    """ Детальная информация о канале"""

    def get(self, request, channel_pk):
        channel = get_channel(channel_pk=channel_pk)
        return Response(get_serializer_data(channel), status=status.HTTP_200_OK)

    def put(self, request, channel_pk):
        channel = update_channel(channel_pk=channel_pk, request=request)
        return Response(get_serializer_data(channel), status=status.HTTP_200_OK)

    def delete(self, request, channel_pk):
        delete_channel(channel_pk=channel_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DeleteUserFromChannel(APIView):
    """ Удаление администратором пользователя из группы """

    def delete(self, request, channel_pk, user_pk):
        channel = delete_user_from_channel_by_admin(user_pk=user_pk, admin=request.user,
                                                         channel_pk=channel_pk)
        return Response(get_serializer_data(channel), status=status.HTTP_204_NO_CONTENT)


class AddOrDeleteFromChannel(APIView):
    """ Отписаться или подписаться на канал """

    def put(self, request, channel_pk):
        response = add_or_delete_user_from_channel(channel_pk=channel_pk, user=request.user)
        if response['subscribe']:
            return Response(get_serializer_data(response['channel']), status.HTTP_201_CREATED)
        else:
            return Response(get_serializer_data(response['channel']), status.HTTP_204_NO_CONTENT)


class CreatePost(APIView):
    """ Публиация постов """

    def post(self, request, channel_pk):
        channel = create_post(request=request, channel_pk=channel_pk)
        return Response(get_serializer_data(channel), status=status.HTTP_201_CREATED)


class PostDetail(APIView):
    """ Детальная информация о посте """

    def put(self, request, post_pk):
        response = update_post(request=request, post_pk=post_pk)
        data = PostSerializer(response).data
        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, post_pk):
        channel = delete_post(post_pk=post_pk, admin=request.user)
        return Response(get_serializer_data(channel), status=status.HTTP_204_NO_CONTENT)


class PostPhotoList(APIView):
    """ Публикация фотографий, которые прикрепляют к посту """

    def post(self, request):
        channel = create_image_post(request=request)
        return Response(get_serializer_data(channel), status=status.HTTP_201_CREATED)


class CommentList(APIView):
    """ Публикация коментариев поста """

    def post(self, request):
        channel = create_comment(request=request)
        return Response(get_serializer_data(channel), status=status.HTTP_201_CREATED)


class CommentDetail(APIView):
    """ Редактирование и удаление коментариев """

    def put(self, request, comment_pk):
        channel = update_comment(request=request, comment_pk=comment_pk)
        return Response(get_serializer_data(channel), status=status.HTTP_200_OK)

    def delete(self, request, comment_pk):
        channel = delete_comment(comment_pk=comment_pk, user=request.user)
        return Response(get_serializer_data(channel), status=status.HTTP_204_NO_CONTENT)


class AddAdmin(APIView):
    """ Добавление админа создателем канала """

    def post(self, request):
        channel = add_admin_in_channel_by_creator(request=request)
        return Response(get_serializer_data(channel), status=status.HTTP_201_CREATED)


class DeleteAdmin(APIView):
    """ Удаление админа создателем канала """

    def delete(self, request):
        channel = delete_admin_from_channel_by_creator(request=request)
        return Response(get_serializer_data(channel), status=status.HTTP_204_NO_CONTENT)
