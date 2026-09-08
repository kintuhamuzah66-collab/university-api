from rest_framework.views import APIView
from rest_framework.response import Response
from courses.models import Course
from courses.serializers import CourseSerializer
from rest_framework import status, viewsets

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer



