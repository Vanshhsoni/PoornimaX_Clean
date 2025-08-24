import os

# 1️⃣ Set settings module first
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poornimax.settings')

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import chat.routing  # safe, only routing patterns

# 2️⃣ Set up ASGI application
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
