from rest_framework.test import APITestCase
from rest_framework import status

from channel.models import Channel, Post, Comment
from account.models import AdvUser

from django.urls import reverse
from config.global_services import sql_processing


class ChannelViewTest(APITestCase):

    def setUp(self):
        self.image = 'static/messenger/images/default_image.jpg'
        self.user_creator = AdvUser.objects.create_user(
            username='creator',
            password='3www1234',
            last_name='Stepan',
            first_name='Murathanov',
            about_user='Люблю работать',
            telephone='89876873914',
            is_verified=True
        )
        self.user = AdvUser.objects.create_user(username='Stepan', password='3www1234', is_verified=True)
        self.channel = Channel.objects.create(
            title='Stepan',
            avatar=self.image,
            description='Stepan',
            creator=self.user_creator,
        )
        self.post = Post.objects.create(text='text', channel=self.channel)
        self.comment = Comment.objects.create(text='Comment', post=self.post, author=self.user_creator)
        #  Для тестирования базы sql запросов закомментировать, чтобы тесты работали быстрее
        # for i in range(20):
        #     Post.objects.create(text='text', channel=self.channel)
        #     Comment.objects.create(text='Comment', post=self.post, author=self.user_creator)
        #     AdvUser.objects.create_user(username='Stepanss%s' % str(i), password='3www1234', is_verified=True)

        url = reverse('account:token_obtain_pair')
        response = self.client.post(url, {'username': 'creator', 'password': '3www1234'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    @sql_processing
    def test_view_channels_of_user(self):
        url = reverse('channel:channels_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_create_channel(self):
        url = reverse('channel:channels_list')
        data = {
            'title': 'Stepan',
            'avatar': self.image,
            'description': 'Stepan',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_get_channel(self):
        url = reverse('channel:channel_detail', kwargs={'channel_pk': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_put_channel(self):
        url = reverse('channel:channel_detail', kwargs={'channel_pk': 1})
        data = {
            'title': 'Stephany',
            'description': "Stepan's channels",
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_channel_delete(self):
        url = reverse('channel:channel_detail', kwargs={'channel_pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_add_delete_user_from_channel_subscribe(self):
        url = reverse('channel:subscriptions_user', kwargs={'channel_pk': 1})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_add_delete_user_from_channel_unsubscribe(self):
        self.client.put(reverse('channel:subscriptions_user', kwargs={'channel_pk': 1}))
        url = reverse('channel:subscriptions_user', kwargs={'channel_pk': self.channel.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_delete_user_by_admin(self):
        url = reverse('channel:delete_user_by_admin',
                      kwargs={'channel_pk': self.channel.pk, 'user_pk': 2})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_post_create(self):
        url = reverse('channel:post_list', kwargs={'channel_pk': 1})
        data = {
            'text': 'text'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_post_put(self):
        url = reverse('channel:post_detail', kwargs={'post_pk': 1})
        data = {
            'text': 'text edited'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_post_delete(self):
        url = reverse('channel:post_detail', kwargs={'post_pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_post_photo_create(self):
        url = reverse('channel:post_photo_list')
        data = {
            'image': self.image,
            'post_pk': 1
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_post_comment_create(self):
        url = reverse('channel:comment_create')
        data = {
            'text': 'This is my comment',
            'post_pk': 1
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_post_comment_put(self):
        url = reverse('channel:comment_detail', kwargs={'comment_pk': self.comment.pk})
        data = {
            'text': 'This is my edit comment',
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_post_comment_delete(self):
        url = reverse('channel:comment_detail', kwargs={'comment_pk': self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_add_admin_by_creator(self):
        url = reverse('channel:add_admin')
        data = {
            'channel_pk': 1,
            'admin_pk': 1,
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_delete_admin_by_creator(self):
        url = reverse('channel:delete_admin')
        data = {
            'channel_pk': 1,
            'admin_pk': 1,
        }
        # Сначала добавим пользователя в админы
        self.client.post(reverse('channel:add_admin'), data=data)
        response = self.client.delete(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
