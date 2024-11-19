from django.db import models
from django.core.validators import MaxValueValidator

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minima = models.DurationField()
    porcentaje_anticipo = models.PositiveIntegerField(default=50, validators=[MaxValueValidator(100)])
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)

    def __str__(self):
        return self.nombre