from django.urls import path
"""

from django.urls import path
from students.api_views import StudentListCreateView, StudentDetailView

urlpatterns = [
    path(
        "students/",
        StudentListCreateView.as_view(),
        name="student-list-create"
    ),
    path(
        "students/<int:pk>/",
        StudentDetailView.as_view(),
        name="student-detail"
    ),
]
"""

from rest_framework.routers import DefaultRouter
from students.api_views import StudentViewSet, StudentAPIView, StudentDetailAPIView

router = DefaultRouter()

router.register(
    'students',
    StudentViewSet,
    basename="student"
)

urlpatterns = router.urls


