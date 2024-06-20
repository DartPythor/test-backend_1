from django.urls import path

from projectsAPI.views import DetailProjectAPI


app_name = "projects"
urlpatterns = [
    path("api/v1/<int:pk>/", DetailProjectAPI.as_view(), name="detail_view"),
]
