from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('Debe ingresar una dirección de correo'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=100)
    apellido_paterno = models.CharField(_('apellido paterno'), max_length=100)
    apellido_materno = models.CharField(_('apellido materno'), max_length=100)
    fecha_registro = models.DateTimeField(_('fecha de registro'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
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