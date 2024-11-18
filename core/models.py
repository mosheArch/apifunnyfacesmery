from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError(_('Debe ingresar una dirección de correo'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Creates and saves a new super user"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=100)
    apellido_paterno = models.CharField(_('apellido paterno'), max_length=100)
    apellido_materno = models.CharField(_('apellido materno'), max_length=100)
    fecha_registro = models.DateTimeField(_('fecha de registro'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=False)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'apellido_paterno', 'apellido_materno']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        app_label = 'core'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.name} {self.apellido_paterno} {self.apellido_materno}"

    def get_short_name(self):
        return self.name

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_minima = models.DurationField()
    porcentaje_anticipo = models.PositiveIntegerField(default=50, validators=[MaxValueValidator(100)])
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)

    def __str__(self):
        return self.nombre

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

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    es_personalizable = models.BooleanField(default=False)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class MetodoPago(models.Model):
    TIPOS = (
        ('transferencia', 'Transferencia Bancaria'),
        ('paypal', 'PayPal'),
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    datos_transferencia = models.TextField(blank=True, null=True)
    enlace_paypal = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.get_tipo_display()

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

    def save(self, *args, **kwargs):
        if self.estado == 'confirmada' and self.pk is None:
            self.curso.cupos_disponibles -= 1
            self.curso.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inscripción de {self.usuario.email} en {self.curso.nombre}"

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