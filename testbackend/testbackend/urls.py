from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("images/", include("imagesAPI.urls")),
    path("projects/", include("projectsAPI.urls")),
]
