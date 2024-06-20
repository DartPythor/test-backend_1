from django.db import models


class Project(models.Model):
    title = models.CharField(
        "название",
        max_length=255,
        help_text="Укажите название проекта.",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "проект"
        verbose_name_plural = "проекты"


__all__ = ()
