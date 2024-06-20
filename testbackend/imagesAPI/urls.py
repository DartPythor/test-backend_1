from django.urls import path

from imagesAPI.views import ImageCreateAPI


app_name = "images"
urlpatterns = [
    path("api/v1/create/", ImageCreateAPI.as_view(), name="create_view"),
]
