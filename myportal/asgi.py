# # myportal/asgi.py
# import os
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportal.settings')
#
# def get_application():
#     from django.core.asgi import get_asgi_application
#     from channels.routing import ProtocolTypeRouter, URLRouter
#     from channels.auth import AuthMiddlewareStack
#     from main.routing import websocket_urlpatterns
#
#     return ProtocolTypeRouter({
#         "http": get_asgi_application(),
#         "websocket": AuthMiddlewareStack(
#             URLRouter(
#                 websocket_urlpatterns
#             )
#         ),
#     })
#
# application = get_application()

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
# import myportal.routing
import main.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportal.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(main.routing.websocket_urlpatterns)
    ),
})