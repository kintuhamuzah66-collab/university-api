from rest_framework import serializers
from students.models import Student
from departments.models import Department

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"

    def validate(self, attrs):
        if attrs.get("firstname") == attrs.get("surname"):
            raise serializers.ValidationError(
                "Student firstname and surname cannot be the same"
            )
        return attrs

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [
            "id",
            "name"
        ]

class GetStudentSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    class Meta:
        model = Student
        fields = "__all__"