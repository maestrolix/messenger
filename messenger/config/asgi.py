import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from config.routing import websockets

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "messenger.settings")

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": websockets,
})
