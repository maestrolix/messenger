from rest_framework.test import APITestCase
from rest_framework import status

from account.models import AdvUser, AvatarImageProfile

from django.urls import reverse
from config.global_services import sql_processing


class AccountViewTest(APITestCase):

    def setUp(self):
        self.image = 'static/messenger/images/default_image.jpg'
        self.user = AdvUser.objects.create_user(
            username='stepan',
            password='3www1234',
            last_name='Stepan',
            first_name='Murathanov',
            about_user='Люблю работать',
            telephone='89876873914',
            is_verified=True
        )
        self.user_avatar = AvatarImageProfile.objects.create(image=self.image, user_id=self.user.id)
        self.user_not_verified = AdvUser.objects.create_user(username='Verified', key=124125234141234)
        #  Для тестирования базы sql запросов закомментировать, чтобы тесты работали быстрее
        # for i in range(15):
        #     AdvUser.objects.create_user(username='stepan%s' % i, is_verified=True)
        #     AvatarImageProfile.objects.create(
        #         image=self.image,
        #         user_id=self.user.id
        #     )
        # Проходим аутенфикацию нового пользователя
        url = reverse('account:token_obtain_pair')
        response = self.client.post(url, {'username': 'stepan', 'password': '3www1234'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    @sql_processing
    def test_view_registration_ok(self):
        url = reverse('account:register')
        data = {
            "username": "stepan125",
            "password": "3www1234",
            "email": "stepan.murathanov@mail.ru"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_confirm_email(self):
        url_key = reverse('account:confirm_account', kwargs={'key': self.user_not_verified.key})
        response = self.client.get(url_key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_registration_error(self):
        url = reverse('account:register')
        data = {
            "usernamess": "Stepan2",
            "password": "3www1234",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @sql_processing
    def test_view_get_auth_profile(self):
        url = reverse('account:auth_user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_put_auth_profile(self):
        url = reverse('account:auth_user')
        data = {
            "username": "Stepanus",
            "last_name": "Murathanyn",
            "fffffirst_name": "SSSStepan"
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_get_profile(self):
        url = '/account/api/profile/%s/' % self.user.id
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_publish_photo_of_user(self):
        url = reverse('account:publish_photo')
        data = {
            "image": self.image
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_delete_photo_of_user_ok(self):
        url = '/account/api/photo_of_user/%s/' % 1
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_delete_photo_of_user_not_found(self):
        url = '/account/api/photo_of_user/%s/' % 1000
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
