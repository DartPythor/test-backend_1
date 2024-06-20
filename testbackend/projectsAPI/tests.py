from pathlib import Path
import tempfile

from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings, TestCase
from django.urls import reverse

from projectsAPI.models import Project
from testbackend.asgi import application


@override_settings(MEDIA_ROOT=tempfile.mktemp())
class TestProjectViewAPI(TestCase):
    fixtures = ["fixtures/data_images.json"]

    @classmethod
    def setUpTestData(cls):
        cls.project = Project.objects.get(id=1)

    def create_image(self):
        with Path("fixtures/test_image.png").open(mode="rb") as file:
            file_image = file.read()
        return self.client.post(
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

    def test_get_image_by_project(self):
        response = self.client.get(
            reverse("projects:detail_view", kwargs={"pk": self.project.id}),
        )
        self.assertEquals(response.status_code, 200)
        self.assertIn("title", response.data)
        self.assertIn("images", response.data)
        self.assertEquals(len(response.data["images"]), 5)
        self.assertIn("image_id", response.data["images"][0])
        self.assertIn("status", response.data["images"][0])
        self.assertIn("project_id", response.data["images"][0])
        self.assertIn("versions", response.data["images"][0])
        self.assertIn("image_id", response.data["images"][0])
        self.assertIn("original", response.data["images"][0]["versions"])
        self.assertIn("thumb", response.data["images"][0]["versions"])
        self.assertIn("big_thumb", response.data["images"][0]["versions"])
        self.assertIn("big_1920", response.data["images"][0]["versions"])
        self.assertIn("d2500", response.data["images"][0]["versions"])

    async def test_create_image_proccesering(self):
        ws_communicator = WebsocketCommunicator(application, "ws/project/1")
        await ws_communicator.connect()
        await sync_to_async(self.create_image)()
        message = await ws_communicator.receive_json_from()
        self.assertEquals(message["status"], "init")
        self.assertEquals(message["filename"], "test_file.png")
        message = await ws_communicator.receive_json_from()
        self.assertEquals(message["status"], "processing")
        self.assertEquals(message["filename"], "test_file.png")
        message = await ws_communicator.receive_json_from()
        self.assertEquals(message["status"], "uploaded")
        self.assertEquals(message["filename"], "test_file.png")
        message = await ws_communicator.receive_json_from()
        self.assertEquals(message["status"], "done")
        self.assertEquals(message["filename"], "test_file.png")


__all__ = ()
