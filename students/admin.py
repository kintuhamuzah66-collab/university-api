from datetime import date

from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):

    @admin.action(description="Deactivate selected students")
    def deactivate_students(modeladmin, request, queryset):
        queryset.update(is_active=False)

    list_display = (
        "firstname",
        "surname",
        "email",
        "date_of_birth",
        "age",
        "department",
        "is_active",
    )

    search_fields = (
        "firstname",
        "surname",
        "email",
        "department__name"
    )

    actions = [
        deactivate_students,
    ]

    list_filter = (
        "department",
        "date_of_birth"
        
    )
    list_per_page = 25

    readonly_fields = (
        "email",
    )
    list_select_related = (
        "department",
    )

    ordering = (
        "surname",
        "firstname",
    )
    ordering = (
        "surname",
        "firstname",
    )

    date_hierarchy = "date_of_birth"

    def age(self, obj):
        today = date.today()

        return (
            today.year
            - obj.date_of_birth.year
            - (
                (today.month, today.day)
                <
                (obj.date_of_birth.month, obj.date_of_birth.day)
            )
        )
    fieldsets = (
        (
            "Personal Information", 
            {
                "fields": (
                    "firstname",
                    "surname",
                    "full_name",
                    "date_of_birth",
                )
            },
        ),
        (
            "Academic Information",
            {
                "fields": (
                    "department",
                    "is_active",
                )
            },
        ),
        (
            "Contact Information",
            {
                "fields": (
                    "email",
                )
            },
        ),
    )
