from account.serializers import AdvUserDetailSerializer
from account.account_services import *
from account.models import AdvUser

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes, api_view


class Register(APIView):
    """ Регистрация пользователей """
    permission_classes = [AllowAny]

    def post(self, request):
        response = registration_user(request=request)
        data = AdvUserDetailSerializer(response).data
        return Response(data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def confirm_account(request, key):
    user = AdvUser.objects.filter(key=key).first()
    user.is_verified = True
    user.key = 0
    user.save(update_fields=['is_verified', 'key'])
    return Response(status=status.HTTP_200_OK)


class CurrentProfile(APIView):
    """ Информация об аутентифицированном пользователе и его редактирование """

    def get(self, request):
        serializer = AdvUserDetailSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = update_user(request=request)
        data = AdvUserDetailSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)


class Profile(APIView):
    """ Информация о выбранном пользователе """

    def get(self, request, user_pk):
        profile = get_profile_of_user(user_pk)
        data = AdvUserDetailSerializer(profile).data
        return Response(data, status=status.HTTP_200_OK)


class PublishPhotoOfUser(APIView):
    """ Публикация фотографий на стене пользователя """

    def post(self, request):
        create_photo_user(data=request.data, user=request.user)
        data = AdvUserDetailSerializer(request.user).data
        return Response(data, status=status.HTTP_201_CREATED)


class DeletePhotoOfUser(APIView):
    """ Удаление фотографии пользователя """

    def delete(self, request, photo_pk):
        delete_photo_user(photo_pk=photo_pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
