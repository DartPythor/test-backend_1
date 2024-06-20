from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from imagesAPI.images_tools import resize_image
from imagesAPI.models import Image
from projectsAPI.models import Project


class ImageSerializers(serializers.Serializer):
    filename = serializers.CharField(
        required=True,
        max_length=100,
    )
    project_id = serializers.IntegerField(
        required=True,
    )
    image = serializers.ImageField(
        required=True,
    )

    @staticmethod
    def send_status(project_channel, group_name, status, filename):
        async_to_sync(project_channel.group_send)(
            group_name,
            {
                "type": "send_status_image",
                "status": status,
                "filename": filename,
            },
        )

    def create(self, validated_data):
        project = get_object_or_404(Project, pk=validated_data["project_id"])
        project_channel = get_channel_layer()
        group_name = f"project_id_{validated_data['project_id']}"
        image = Image.objects.create(
            project=project,
            status="init",
        )
        try:
            self.send_status(
                project_channel,
                group_name,
                "init",
                validated_data["filename"],
            )
            self.send_status(
                project_channel,
                group_name,
                "processing",
                validated_data["filename"],
            )
            image.original = validated_data["image"]
            image.thumb = resize_image(validated_data["image"], 150, 20)
            image.big_thumb = resize_image(validated_data["image"], 700, 700)
            image.big_1920 = resize_image(validated_data["image"], 1920, 1080)
            image.d2500 = resize_image(validated_data["image"], 2500, 2500)
            image.status = "uploaded"
            image.save()
            self.send_status(
                project_channel,
                group_name,
                "uploaded",
                validated_data["filename"],
            )
            image.status = "done"
            image.save()
            self.send_status(
                project_channel,
                group_name,
                "done",
                validated_data["filename"],
            )
            return {
                "filename": validated_data["filename"],
                "project_id": validated_data["project_id"],
                "image": image.original,
            }
        except Exception as error:
            self.send_status(
                project_channel,
                group_name,
                "error",
                validated_data["filename"],
            )
            image.status = "error"
            image.save()
            raise error


class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


__all__ = ()
