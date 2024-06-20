import io

from django.core.files.uploadedfile import InMemoryUploadedFile
import PIL.Image


def resize_image(image, width, height):
    img = PIL.Image.open(image)
    img = img.resize((width, height), PIL.Image.Resampling.LANCZOS)
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, image.name.split(".")[-1])
    img_byte_arr = img_byte_arr.getvalue()

    return InMemoryUploadedFile(
        io.BytesIO(img_byte_arr),
        field_name="image",
        name=image.name,
        content_type=image.content_type,
        size=len(img_byte_arr),
        charset=None,
    )


__all__ = ()
