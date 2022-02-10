from rest_framework.test import APITestCase
from rest_framework import status

from account.models import AdvUser

from thread.models import Thread, Message

from django.urls import reverse
from config.global_services import sql_processing


class ThreadViewTest(APITestCase):

    def setUp(self):
        self.image = 'static/messenger/images/default_image.jpg'
        self.user1 = AdvUser.objects.create_user(username='Stepan', password='3www1234', is_verified=True)
        self.user2 = AdvUser.objects.create_user(username='Stepan2', password='3www1234', is_verified=True)
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(thread=self.thread, text='My name is Stephan', author=self.user1)
        #  Для тестирования базы sql запросов закомментировать, чтобы тесты работали быстрее
        # for i in range(40):
        #     AdvUser.objects.create_user(username='stepo%s' % i, password='3www123%s' % i, is_verified=True)
        #     thread = Thread.objects.create()
        #     thread.participants.add(self.user1, self.user2)
        #     message = Message.objects.create(thread=self.thread, text='My name is Stephan', author=self.user1)
        #     thread.last_message = message
        #     thread.save(update_fields=['last_message'])
        # threads = Thread.objects.all()[10:20]
        # for thread in threads:
        #     thread.archive.add(self.user1)
        # Проходим аутентификацию нового пользователя
        url = reverse('account:token_obtain_pair')
        response = self.client.post(url, {'username': 'Stepan', 'password': '3www1234'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    @sql_processing
    def test_view_get_active_threads(self):
        url = reverse('thread:thread_list') + '?type=active'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_get_archive_threads(self):
        url = reverse('thread:thread_list') + '?type=archive'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_thread_create(self):
        url = reverse('thread:thread_list')
        data = {
            'participants': [1, 2]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_get_thread(self):
        url = reverse('thread:thread_detail', kwargs={'thread_pk': self.thread.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_put_thread_push_notification(self):
        url = reverse('thread:push_notif', kwargs={'thread_pk': self.thread.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_thread_for_auth_user_delete(self):
        url = reverse('thread:thread_delete', kwargs={'thread_pk': self.thread.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_put_thread_archive(self):
        url = reverse('thread:thread_archive', kwargs={'thread_pk': self.thread.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_message_create(self):
        url = reverse('thread:message_list')
        data = {
            'thread_id': self.thread.pk,
            'text': 'Hello world!'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @sql_processing
    def test_view_message_put(self):
        url = reverse('thread:message_detail', kwargs={'message_pk': self.message.pk})
        data = {
            'text': 'Goodbye world!'
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @sql_processing
    def test_view_message_for_auth_user_delete(self):
        url = reverse('thread:message_list')
        data = {
            'message_ids': [1]
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_message_delete(self):
        url = reverse('thread:message_list')
        data = {
            'message_ids': [1, 2, 3, 10]
        }
        response = self.client.delete(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @sql_processing
    def test_view_message_image_create(self):
        url = reverse('thread:photo_list')
        data = {
            'message_id': self.message.pk,
            'images': [self.image, self.image, self.image, self.image, self.image]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
