from django.db import models
from departments.models import Department
from lecturers.models import Lecturer


class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=100)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    lecturer = models.ForeignKey(
        Lecturer,
        on_delete=models.PROTECT,
        related_name="courses"
    )

    def __str__(self):
        return f"{self.code} - {self.title}"