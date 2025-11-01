from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NetworkNodeViewSet, api_test_view

router = DefaultRouter()
router.register(r"network-nodes", NetworkNodeViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-test/", api_test_view, name="api-test"),
]
