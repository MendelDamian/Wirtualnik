from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserCreateViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)

urlpatterns = router.urls
