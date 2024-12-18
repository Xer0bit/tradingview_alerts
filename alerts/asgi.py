# tradingview_alerts/asgi.py
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import alerts.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradingview_alerts.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # HTTP protocol for standard requests
    "websocket": AuthMiddlewareStack(  # WebSocket protocol for WebSocket requests
        URLRouter(
            alerts.routing.websocket_urlpatterns
        )
    ),
})
