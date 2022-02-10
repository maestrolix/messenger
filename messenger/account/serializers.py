from rest_framework import serializers
from account.models import AdvUser, AvatarImageProfile


class AvatarImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvatarImageProfile
        exclude = ('user', 'id',)


class AdvUserDetailSerializer(serializers.ModelSerializer):
    profile_avatars = AvatarImageProfileSerializer(many=True)
    username = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = AdvUser
        fields = ["id", "last_active", "get_full_name",
                  "is_online", "first_name",
                  "last_name", "about_user", "username",
                  "telephone", "profile_avatars"
                  ]


class AdvUserListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = AdvUser
        fields = ["get_full_name", 'username']


