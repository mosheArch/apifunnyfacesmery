from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _


def comprobante_directory_path(instance, filename):
    # Obtenemos la fecha actual
    from django.utils import timezone
    now = timezone.now()
    # Creamos una estructura de carpetas basada en la fecha y el tipo de comprobante
    if isinstance(instance, InscripcionCurso):
        return f'comprobantes/cursos/{now.year}/{now.month:02d}/{instance.curso.id}/{filename}'
    elif isinstance(instance, Reserva):
        return f'comprobantes/servicios/{now.year}/{now.month:02d}/{instance.servicio.id}/{filename}'
    elif isinstance(instance, Pedido):
        return f'comprobantes/pedidos/{now.year}/{now.month:02d}/{instance.usuario.name}/{filename}'

def temario_directory_path(instance, filename):
        # El archivo se subirá a MEDIA_ROOT/temarios/curso_<id>/<filename>
        return f'temarios/curso_{instance.id}/{filename}'

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
    apellido_paterno = models.CharField(_('apellido paterno'), max_length=100, null=True, blank=True,)
    apellido_materno = models.CharField(_('apellido materno'), max_length=100, null=True, blank=True,)
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
    duracion = models.CharField(max_length=50)
    precio_base = models.DecimalField(max_digits=8, decimal_places=2)
    url_imagen = models.URLField()

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    TIPOS = (
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    duracion = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    cupos_disponibles = models.PositiveIntegerField()
    url_imagen = models.URLField()
    tipo = models.CharField(max_length=10, choices=TIPOS)
    temario_pdf = models.FileField(
        upload_to=temario_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        null=True,
        blank=True,
        help_text="Sube el temario del curso en formato PDF"
    )

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    url_imagen = models.URLField()
    personalizable = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('revision', 'En revisión'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    codigo_postal = models.CharField(max_length=5)
    precio_total = models.DecimalField(max_digits=8, decimal_places=2)
    monto_deposito = models.DecimalField(max_digits=8, decimal_places=2)
    comprobante_anticipo = models.FileField(
        upload_to=comprobante_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Sube el comprobante de pago del anticipo",
        null = True,
        blank = True
    )
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')

    def __str__(self):
        return f"Reserva de {self.usuario.email} para {self.servicio.nombre}"

class InscripcionCurso(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('revision', 'En revisión'),
        ('confirmada', 'Confirmada'),
        ('cancelada', 'Cancelada'),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=8, decimal_places=2)
    monto_deposito = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    comprobante_anticipo = models.FileField(
        upload_to=comprobante_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Sube el comprobante de pago del anticipo",
        null = True,
        blank = True
    )

    def __str__(self):
        return f"Inscripción de {self.usuario.email} en {self.curso.nombre}"

class Pedido(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('revision', 'En revisión'),
        ('procesando', 'Procesando'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    precio_total = models.DecimalField(max_digits=8, decimal_places=2)
    monto_deposito = models.DecimalField(max_digits=8, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente')
    url_rastreo = models.URLField(blank=True, null=True)
    comprobante_anticipo = models.FileField(
        upload_to=comprobante_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text="Sube el comprobante de pago del anticipo",
        null = True,
        blank = True
    )

    def __str__(self):
        return f"Pedido #{self.id} de {self.usuario.email}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    notas_personalizacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} en Pedido #{self.pedido.id}"

