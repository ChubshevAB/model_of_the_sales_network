from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class NetworkNode(models.Model):
    """Модель узла сети электроники"""

    LEVEL_CHOICES = [
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Уровень иерархии")

    # Контакты
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")

    # Продукты
    product_name = models.CharField(max_length=255, verbose_name="Название продукта")
    product_model = models.CharField(max_length=255, verbose_name="Модель продукта")
    product_release_date = models.DateField(
        verbose_name="Дата выхода продукта на рынок"
    )

    # Поставщик
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Поставщик",
    )

    # Задолженность
    debt_to_supplier = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Задолженность перед поставщиком",
        default=0.00,
    )

    # Время создания
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    # Активность сотрудника
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    class Meta:
        verbose_name = "Узел сети"
        verbose_name_plural = "Узлы сети"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_level_display()}: {self.name}"

    def save(self, *args, **kwargs):
        # Автоматическое определение уровня на основе поставщика
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0  # Завод
        super().save(*args, **kwargs)
