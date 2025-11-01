from rest_framework import serializers
from .models import NetworkNode


class NetworkNodeSerializer(serializers.ModelSerializer):
    level_display = serializers.CharField(source="get_level_display", read_only=True)

    class Meta:
        model = NetworkNode
        fields = [
            "id",
            "name",
            "level",
            "level_display",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "product_name",
            "product_model",
            "product_release_date",
            "supplier",
            "debt_to_supplier",
            "created_at",
            "is_active",
        ]
        read_only_fields = ["debt_to_supplier", "created_at"]
