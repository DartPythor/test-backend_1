from django.urls import path

from projectsAPI.consumers import AIConsumer

websocket_urlpatterns = [
    path("ws/project/<int:pk>", AIConsumer.as_asgi()),
]
