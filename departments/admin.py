from django.contrib import admin
from .models import Department
from students.models import Student


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
    ]