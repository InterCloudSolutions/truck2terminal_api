from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TerminalViewSet

app_name = "terminals"

router = DefaultRouter()
router.register(r"", TerminalViewSet, basename="terminal")

urlpatterns = [
    path("", include(router.urls)),
]
