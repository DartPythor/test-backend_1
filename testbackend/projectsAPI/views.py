from rest_framework.generics import RetrieveAPIView

from projectsAPI.models import Project
from projectsAPI.serializers import ProjectSerializer


class DetailProjectAPI(RetrieveAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()


__all__ = ()
