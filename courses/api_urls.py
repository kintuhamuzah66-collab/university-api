from rest_framework.routers import DefaultRouter
from courses.api_views import CourseViewSet
from django.urls import path 

router = DefaultRouter()

router.register(
    "courses",
    CourseViewSet,
    basename="course"
)

urlpatterns = router.urls


