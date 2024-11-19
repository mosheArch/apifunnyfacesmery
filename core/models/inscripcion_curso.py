from django.db import models
from .user import User
from .curso import Curso
from .metodo_pago import MetodoPago

class InscripcionCurso(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    comprobante_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    paypal_order_id = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.estado == 'confirmada' and self.pk is None:
            self.curso.cupos_disponibles -= 1
            self.curso.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inscripción de {self.usuario.email} en {self.curso.nombre}"

    def registrar_pago(self, monto, metodo_pago, estado, detalles=None):
        from .bitacora_pago import BitacoraPago
        BitacoraPago.objects.create(
            usuario=self.usuario,
            tipo_compra='curso',
            id_compra=self.id,
            monto=monto,
            metodo_pago=metodo_pago,
            estado=estado,
            detalles=detalles
        )