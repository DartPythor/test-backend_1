from rest_framework import generics

from imagesAPI.serializers import ImageSerializers


class ImageCreateAPI(generics.CreateAPIView):
    serializer_class = ImageSerializers


__all__ = ()
