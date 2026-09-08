from django.db import models
from departments.models import Department


class Lecturer(models.Model):
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="lecturers"
    )

    def __str__(self):
        return f"{self.firstname} {self.surname}"