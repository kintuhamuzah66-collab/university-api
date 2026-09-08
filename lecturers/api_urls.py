from rest_framework.routers import DefaultRouter
from .api_views import LecturerViewSet

router = DefaultRouter()
router.register(
    "lecturers",
    LecturerViewSet,
    basename="lecturer"
)

urlpatterns = router.urls