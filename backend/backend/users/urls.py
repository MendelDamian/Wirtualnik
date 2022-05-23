from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, UserCreateViewSet, UpdatePasswordAPIView

app_name = "backend.users"

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"users", UserCreateViewSet)

urlpatterns = router.urls

urlpatterns += [
    path("change-password/", UpdatePasswordAPIView.as_view(), name="change-password"),
]
