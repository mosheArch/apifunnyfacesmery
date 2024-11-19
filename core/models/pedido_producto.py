from django.db import models
from core.models.user import User
from core.models.producto import Producto
from core.models.metodo_pago import MetodoPago

class PedidoProducto(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente de pago'),
        ('pagado', 'Pagado'),
        ('en_proceso', 'En Proceso'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    personalizacion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True)
    comprobante_pago = models.FileField(upload_to='comprobantes/', null=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.precio_total:
            self.precio_total = self.producto.precio * self.cantidad
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido de {self.usuario.email} - {self.producto.nombre}"

    def registrar_pago(self, monto, metodo_pago, estado, detalles=None):
        from core.models.bitacora_pago import BitacoraPago
        BitacoraPago.objects.create(
            usuario=self.usuario,
            tipo_compra='producto',
            id_compra=self.id,
            monto=monto,
            metodo_pago=metodo_pago,
            estado=estado,
            detalles=detalles
        )