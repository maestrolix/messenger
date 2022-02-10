from rest_framework import serializers

from channel.models import *
from account.serializers import AdvUserDetailSerializer, AdvUserListSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = AdvUserListSerializer()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only = ['pk', 'author', 'created_at', 'post']
        extra_kwargs = {'author': {'required': False},
                        'post': {'required': False}}


class PostPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImagePost
        fields = '__all__'
        extra_kwargs = {'sender': {'required': False}}


class PostSerializer(serializers.ModelSerializer):
    # post_comments = CommentSerializer(many=True, required=False)
    # post_images = PostPhotoSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['id', 'text', 'created_at']
        read_only_fields = ['pk', 'post_comments']
        extra_kwargs = {'text': {'required': False}}


class ChannelListSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    creator = AdvUserListSerializer()

    class Meta:
        model = Channel
        fields = ['posts', 'creator']


class ChannelDetailSerializer(serializers.ModelSerializer):
    participants = AdvUserListSerializer(many=True, required=False)
    admins = AdvUserListSerializer(many=True, required=False)
    creator = AdvUserListSerializer()

    class Meta:
        model = Channel
        fields = '__all__'
        extra_kwargs = {'title': {'required': False},
                        'description': {'required': False},
                        'avatar': {'required': False}}
