from django.urls import path

from projectsAPI.consumers import ProjectConsumer

websocket_urlpatterns = [
    path("ws/project/<int:pk>", ProjectConsumer.as_asgi()),
]
