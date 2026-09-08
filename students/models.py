from django.db import models
from departments.models import Department


class Student(models.Model):
    surname = models.CharField(max_length=100)
    firstname = models.CharField(max_length=100)
    full_name = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="students"
    )

    profile_picture = models.ImageField(
        upload_to="student_photos/",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.firstname} {self.surname}"