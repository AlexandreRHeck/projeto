# clinic/routing.py

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/password_updates/$', consumers.PasswordConsumer.as_asgi()),
]
