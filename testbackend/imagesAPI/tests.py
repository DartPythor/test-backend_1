from http import HTTPStatus
from pathlib import Path
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

from imagesAPI.models import Image
from projectsAPI.models import Project


@override_settings(MEDIA_ROOT=tempfile.mktemp())
class TestImageViewAPI(TestCase):
    fixtures = ["fixtures/data.json"]

    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.get(id=1)

    def test_create_image_view(self):
        with Path("fixtures/test_image.png").open(mode="rb") as file:
            file_image = file.read()
        image_count = Image.objects.count()
        response = self.client.post(
            reverse("images:create_view"),
            {
                "filename": "test_file.png",
                "project_id": self.project.id,
                "image": SimpleUploadedFile(
                    name="test_image.png",
                    content=file_image,
                    content_type="image/png",
                ),
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.CREATED)
        self.assertEquals(Image.objects.count(), image_count + 1)

    def test_create_image_without_name(self):
        with Path("fixtures/test_image.png").open(mode="rb") as file:
            file_image = file.read()
        image_count = Image.objects.count()
        response = self.client.post(
            reverse("images:create_view"),
            {
                "project_id": self.project.id,
                "image": SimpleUploadedFile(
                    name="test_image.png",
                    content=file_image,
                    content_type="image/png",
                ),
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("filename", response.data)
        self.assertEquals(Image.objects.count(), image_count)

    def test_create_image_without_project(self):
        with Path("fixtures/test_image.png").open(mode="rb") as file:
            file_image = file.read()
        image_count = Image.objects.count()
        response = self.client.post(
            reverse("images:create_view"),
            {
                "filename": "test_file.png",
                "image": SimpleUploadedFile(
                    name="test_image.png",
                    content=file_image,
                    content_type="image/png",
                ),
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("project_id", response.data)
        self.assertEquals(Image.objects.count(), image_count)

    def test_create_image_without_image(self):
        image_count = Image.objects.count()
        response = self.client.post(
            reverse("images:create_view"),
            {
                "filename": "test_file.png",
                "project_id": self.project.id,
            },
        )
        self.assertEquals(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertIn("image", response.data)
        self.assertEquals(Image.objects.count(), image_count)


__all__ = ()
