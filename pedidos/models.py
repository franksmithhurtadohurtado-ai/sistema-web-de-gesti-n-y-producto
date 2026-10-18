from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Pedido(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = "pendiente", "Pendiente"
        CONFIRMADO = "confirmado", "Confirmado"
        CANCELADO = "cancelado", "Cancelado"

    numero_pedido = models.CharField(
        max_length=20,
        unique=True,
        error_messages={"unique": "Ya existe un pedido con ese número."},
    )
    cliente = models.CharField(max_length=100)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=500)
    valor_total = models.DecimalField(
        max_digits=12, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), "El valor total debe ser mayor que cero.")],
    )
    estado = models.CharField(
        max_length=10, choices=Estado.choices, default=Estado.PENDIENTE
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="pedidos"
    )

    class Meta:
        ordering = ["-fecha_registro"]
        constraints = [
            models.CheckConstraint(
                condition=Q(valor_total__gt=0), name="pedido_valor_total_mayor_que_cero"
            ),
        ]

    def __str__(self):
        return f"Pedido {self.numero_pedido} - {self.cliente}"