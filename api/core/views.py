from rest_framework import viewsets, mixins

from core.models import School
from core.serializers import SchoolSerializer


class SchoolViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer