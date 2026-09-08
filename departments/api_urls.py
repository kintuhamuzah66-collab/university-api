from departments.api_views import DepartmentViewSet 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(
    "departmentss",
    DepartmentViewSet,
    basename="department"
)

urlpatterns = router.urls