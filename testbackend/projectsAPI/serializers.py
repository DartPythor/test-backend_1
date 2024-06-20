from rest_framework.serializers import ModelSerializer

from imagesAPI.serializers import ImageModelSerializer
from projectsAPI.models import Project


class ProjectSerializer(ModelSerializer):
    images = ImageModelSerializer(many=True, read_only=True)

    class Meta:
        fields = ["title", "images"]
        model = Project

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        images_list = []
        for image in representation["images"]:
            new_image = {
                "image_id": image["id"],
                "status": image["status"],
                "project_id": image["project"],
                "versions": {
                    "original": image["original"],
                    "thumb": image["thumb"],
                    "big_thumb": image["big_thumb"],
                    "big_1920": image["big_1920"],
                    "d2500": image["d2500"],
                },
            }
            images_list.append(new_image)
        return {
            "title": representation["title"],
            "images": images_list,
        }


__all__ = ()
