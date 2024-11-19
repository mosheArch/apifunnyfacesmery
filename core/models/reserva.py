from django.db import models
from django.utils import timezone
from core.models.user import User
from core.models.servicio import Servicio
from core.models.metodo_pago import MetodoPago

class Reserva(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente de pago'),
        ('anticipo_pagado', 'Anticipo pagado'),
        ('pagado', 'Pagado completamente'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    direccion_servicio = models.TextField()
    codigo_postal_servicio = models.CharField(max_length=10)
    ciudad_servicio = models.CharField(max_length=100)
    coordenadas = models.CharField(max_length=50, blank=True, null=True)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    comprobante_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.precio_final:
            duracion = timezone.datetime.combine(timezone.datetime.today(), self.hora_fin) - \
                       timezone.datetime.combine(timezone.datetime.today(), self.hora_inicio)
            horas = duracion.total_seconds() / 3600
            self.precio_final = self.servicio.precio_base * max(1, horas)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reserva de {self.usuario.email} para {self.servicio.nombre}"

    def registrar_pago(self, monto, metodo_pago, estado, detalles=None):
        from core.models.bitacora_pago import BitacoraPago
        BitacoraPago.objects.create(
            usuario=self.usuario,
            tipo_compra='servicio',
            id_compra=self.id,
            monto=monto,
            metodo_pago=metodo_pago,
            estado=estado,
            detalles=detalles
        )