from thread.thread_web_socket.routing import websocket_urlpatterns as thread_websocket

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter


websockets = AuthMiddlewareStack(
    URLRouter(
        thread_websocket
    )
)
