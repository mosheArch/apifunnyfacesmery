from django.db import models

class MetodoPago(models.Model):
    TIPOS = (
        ('transferencia', 'Transferencia Bancaria'),
        ('paypal', 'PayPal'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    datos_transferencia = models.TextField(blank=True, null=True)
    cliente_id_paypal = models.CharField(max_length=255, blank=True, null=True)
    secreto_paypal = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.get_tipo_display()