from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # re_path(r'ws/article/(?P<slug>[^/]+)/$', consumers.ArticleConsumer.as_asgi()),
    re_path(r'ws/article/(?P<slug>[\w-]+)/$', consumers.ArticleConsumer.as_asgi()),
]