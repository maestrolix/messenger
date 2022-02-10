from django.urls import path

from thread.thread_web_socket import consumers


websocket_urlpatterns = [
    path('ws/thread/<int:thread_id>/', consumers.MessageConsumer.as_asgi())
]





