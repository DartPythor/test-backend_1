from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class ImagePathUpload:
    def __init__(self, path):
        self.path = path

    def __call__(self, instance, filename):
        return f"{instance.project.id}/{self.path}/{filename}"


class Image(models.Model):
    STATUS_CHOICES = [
        ("init", "иницилизация"),
        ("uploaded", "загруженно"),
        ("processing", "обработка"),
        ("done", "завершенно"),
        ("error", "ошибка"),
    ]
    project = models.ForeignKey(
        "projectsAPI.project",
        related_name="project",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        verbose_name="проект",
        help_text="Выберите проект к которому будет принадлежать изображение.",
    )
    original = models.ImageField(
        upload_to=ImagePathUpload("original"),
    )
    thumb = models.ImageField(
        upload_to=ImagePathUpload("thumbs"),
    )
    big_thumb = models.ImageField(
        upload_to=ImagePathUpload("big_thumbs"),
    )
    big_1920 = models.ImageField(
        upload_to=ImagePathUpload("big_1920"),
    )
    d2500 = models.ImageField(
        upload_to=ImagePathUpload("d2500"),
    )
    status = models.CharField(
        choices=STATUS_CHOICES,
        max_length=10,
        default="init",
    )

    class Meta:
        verbose_name = "избражение"
        verbose_name_plural = "изображения"


__all__ = ()
