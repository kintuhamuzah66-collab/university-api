from rest_framework import viewsets
from departments.serializers import DepartmentSerializer
from departments.models import Department

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


