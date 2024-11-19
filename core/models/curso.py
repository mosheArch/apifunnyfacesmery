from django.db import models

class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion = models.DurationField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    cupos_totales = models.PositiveIntegerField()
    cupos_disponibles = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to='cursos/', null=True, blank=True)

    def __str__(self):
        return self.nombre