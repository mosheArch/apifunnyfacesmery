from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import Servicio, Curso, Producto, Reserva, InscripcionCurso, Pedido, ItemPedido, User
from django.utils.translation import gettext_lazy as _
# Registrar el modelo de Usuario personalizado

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'apellido_paterno', 'apellido_materno')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'apellido_paterno', 'apellido_materno', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'apellido_paterno', 'apellido_materno', 'is_staff')
    search_fields = ('email', 'name', 'apellido_paterno', 'apellido_materno')
    ordering = ('email',)

# Registrar el modelo de Servicio
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion', 'precio_base')
    search_fields = ('nombre',)

# Registrar el modelo de Curso
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'duracion', 'precio', 'cupos_disponibles', 'tipo')
    list_filter = ('tipo',)
    search_fields = ('nombre',)

# Registrar el modelo de Producto
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'personalizable')
    list_filter = ('personalizable',)
    search_fields = ('nombre',)

# Registrar el modelo de Reserva
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'estado')
    list_filter = ('estado', 'fecha_reserva')
    search_fields = ('usuario__email', 'servicio__nombre')

# Registrar el modelo de InscripcionCurso
@admin.register(InscripcionCurso)
class InscripcionCursoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fecha_inscripcion', 'estado')
    list_filter = ('estado', 'fecha_inscripcion')
    search_fields = ('usuario__email', 'curso__nombre')

# Registrar el modelo de Pedido
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha_pedido', 'precio_total', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__email', 'id')

# Registrar el modelo de ItemPedido
@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ('pedido', 'producto', 'cantidad', 'precio')
    search_fields = ('pedido__id', 'producto__nombre')
