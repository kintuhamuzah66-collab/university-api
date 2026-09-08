from rest_framework import serializers
from courses.models import Course
from departments.models import Department
from lecturers.models import Lecturer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"

class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecturer
        fields = [
            "id",
            "firstname",
            "surname",
        ]

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    lecturer = LecturerSerializer(read_only=True)
    class Meta:
        model = Course 
        fields = "__all__"