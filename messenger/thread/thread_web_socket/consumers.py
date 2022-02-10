import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from thread.models import Message, Thread


class MessageConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        self.user = self.scope['user']
        self.post_group_name = 'thread_%s' % self.thread_id

        await self.channel_layer.group_add(
            self.post_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.post_group_name,
            self.channel_name
        )

    async def receive(self, text_data_json):
        text_data = json.loads(text_data_json)
        message = text_data['text']
        new_message = await self.create_new_message(message)
        data = {
            'sender': new_message.author.pk,
            'created_at': new_message.created_at.strftime('%Y-%m-%d %H:%m'),
            'text': new_message.text,
            'message_id': new_message.pk,
        }

        await self.channel_layer.group_send(
            self.post_group_name,
            {
                'type': 'new_message',
                'message': data
            }
        )

    async def new_message(self, event):
        message = event['message']

        await self.send(
            text_data=json.dumps({
                'message': message
            })
        )

    @database_sync_to_async
    def create_new_message(self, message):
        thread = Thread.objects.get(pk=self.thread_id)
        new_message = Message.objects.create(
            author=self.ser,
            text=message,
            thread=thread
        )
        new_message.save(update_fields=['author', 'text', 'thread'])
        return new_message
