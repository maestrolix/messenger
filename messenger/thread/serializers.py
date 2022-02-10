from rest_framework import serializers

from thread.models import *
from account.serializers import AdvUserListSerializer


class MessagePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagePhoto
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    message_photos = MessagePhotoSerializer(many=True, required=False)
    author = AdvUserListSerializer()
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Message
        fields = ['pk', 'text', 'created_at', 'thread', 'message_photos', 'author']


class MessageListSerializer(serializers.ModelSerializer):
    author = AdvUserListSerializer()

    class Meta:
        model = Message
        fields = ['id', 'text', 'created_at', 'author']


class ThreadListSerializer(serializers.ModelSerializer):
    last_message = MessageListSerializer()

    class Meta:
        model = Thread
        fields = ['id', 'last_message']


class ThreadDetailSerializer(serializers.ModelSerializer):
    participants = AdvUserListSerializer(many=True, required=False)
    thread_messages = MessageSerializer(many=True)

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'push_notification', 'thread_messages']
