from django.db import models
from django.utils import timezone
from core.models.user import User
from core.models.metodo_pago import MetodoPago

class BitacoraPago(models.Model):
    TIPOS_COMPRA = (
        ('curso', 'Curso'),
        ('servicio', 'Servicio'),
        ('producto', 'Producto'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo_compra = models.CharField(max_length=20, choices=TIPOS_COMPRA)
    id_compra = models.PositiveIntegerField()  # ID del curso, servicio o producto
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    fecha_pago = models.DateTimeField(default=timezone.now)
    estado = models.CharField(max_length=50)  # Por ejemplo: "completado", "pendiente", "fallido"
    detalles = models.TextField(blank=True, null=True)  # Para almacenar detalles adicionales o ID de transacción

    def __str__(self):
        return f"Pago de {self.usuario.email} - {self.tipo_compra} - {self.fecha_pago}"

    class Meta:
        ordering = ['-fecha_pago']