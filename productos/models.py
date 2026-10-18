from decimal import Decimal

from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Q


class Producto(models.Model):
    nombre = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(3, "El nombre debe tener al menos 3 caracteres.")],
    )
    descripcion = models.CharField(max_length=500, blank=True)
    precio = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"), "El precio debe ser mayor que cero.")],
    )
    cantidad_disponible = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_registro"]
        constraints = [
            models.CheckConstraint(
                condition=Q(precio__gt=0), name="producto_precio_mayor_que_cero"
            ),
        ]

    def __str__(self):
        return self.nombre