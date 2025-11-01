from django.contrib import admin
from django.utils.html import format_html
from .models import NetworkNode


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "level_display",
        "city",
        "debt_to_supplier",
        "supplier_link",
        "created_at",
        "is_active",
    ]
    list_filter = ["city", "country", "level", "is_active"]
    search_fields = ["name", "product_name", "email"]
    list_editable = ["is_active"]
    actions = ["clear_debt"]

    def level_display(self, obj):
        return obj.get_level_display()

    level_display.short_description = "Уровень"

    def supplier_link(self, obj):
        if obj.supplier:
            return format_html(
                '<a href="/admin/electronics/networknode/{}/change/">{}</a>',
                obj.supplier.id,
                obj.supplier.name,
            )
        return "Нет поставщика"

    supplier_link.short_description = "Поставщик"

    def clear_debt(self, request, queryset):
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов")

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

    fieldsets = (
        ("Основная информация", {"fields": ("name", "level", "is_active")}),
        (
            "Контакты",
            {"fields": ("email", "country", "city", "street", "house_number")},
        ),
        (
            "Продукты",
            {"fields": ("product_name", "product_model", "product_release_date")},
        ),
        ("Финансы и связи", {"fields": ("supplier", "debt_to_supplier")}),
    )
