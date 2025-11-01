from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import NetworkNode
from .serializers import NetworkNodeSerializer
from django.shortcuts import render


class IsActiveEmployee(permissions.BasePermission):
    """Разрешение только для активных сотрудников"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all()
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["country"]
    search_fields = ["name", "product_name", "city"]

    def get_queryset(self):
        return NetworkNode.objects.filter(is_active=True)


def api_test_view(request):
    return render(request, "electronics/api_test.html")
