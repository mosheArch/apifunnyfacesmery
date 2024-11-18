from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Servicio, Curso, Producto, MetodoPago, Reserva, InscripcionCurso, PedidoProducto

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'name', 'apellido_paterno', 'apellido_materno', 'is_active', 'is_staff', 'fecha_registro')
    list_filter = ('is_active', 'is_staff', 'fecha_registro')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('name', 'apellido_paterno', 'apellido_materno')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'fecha_registro')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'apellido_paterno', 'apellido_materno', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name', 'apellido_paterno', 'apellido_materno')
    ordering = ('email',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_base', 'duracion_minima', 'porcentaje_anticipo')
    search_fields = ('nombre',)

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'fecha_inicio', 'fecha_fin', 'cupos_disponibles')
    search_fields = ('nombre',)
    list_filter = ('fecha_inicio', 'fecha_fin')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'es_personalizable')
    search_fields = ('nombre',)
    list_filter = ('es_personalizable',)

@admin.register(MetodoPago)
class MetodoPagoAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'descripcion')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha', 'hora_inicio', 'hora_fin', 'precio_final', 'estado', 'monto_pagado')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('usuario__email', 'servicio__nombre')
    actions = ['confirmar_pago_anticipo', 'confirmar_pago_total']

    def confirmar_pago_anticipo(self, request, queryset):
        for reserva in queryset:
            if reserva.estado == 'pendiente' and reserva.comprobante_pago:
                anticipo = reserva.precio_final * (reserva.servicio.porcentaje_anticipo / 100)
                reserva.monto_pagado = anticipo
                reserva.estado = 'anticipo_pagado'
                reserva.save()
    confirmar_pago_anticipo.short_description = "Confirmar pago de anticipo"

    def confirmar_pago_total(self, request, queryset):
        for reserva in queryset:
            if reserva.comprobante_pago:
                reserva.monto_pagado = reserva.precio_final
                reserva.estado = 'pagado'
                reserva.save()
    confirmar_pago_total.short_description = "Confirmar pago total"

@admin.register(InscripcionCurso)
class InscripcionCursoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'curso', 'fecha_inscripcion', 'estado')
    list_filter = ('estado', 'fecha_inscripcion')
    search_fields = ('usuario__email', 'curso__nombre')
    actions = ['confirmar_pago']

    def confirmar_pago(self, request, queryset):
        for inscripcion in queryset:
            if inscripcion.estado == 'pendiente' and inscripcion.comprobante_pago:
                inscripcion.estado = 'pagado'
                inscripcion.save()
    confirmar_pago.short_description = "Confirmar pago"

@admin.register(PedidoProducto)
class PedidoProductoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'producto', 'cantidad', 'precio_total', 'estado')
    list_filter = ('estado', 'fecha_pedido')
    search_fields = ('usuario__email', 'producto__nombre')
    actions = ['confirmar_pago', 'marcar_en_proceso', 'marcar_enviado', 'marcar_entregado']

    def confirmar_pago(self, request, queryset):
        for pedido in queryset:
            if pedido.estado == 'pendiente' and pedido.comprobante_pago:
                pedido.estado = 'pagado'
                pedido.save()
    confirmar_pago.short_description = "Confirmar pago"

    def marcar_en_proceso(self, request, queryset):
        queryset.filter(estado='pagado').update(estado='en_proceso')
    marcar_en_proceso.short_description = "Marcar como en proceso"

    def marcar_enviado(self, request, queryset):
        queryset.filter(estado='en_proceso').update(estado='enviado')
    marcar_enviado.short_description = "Marcar como enviado"

    def marcar_entregado(self, request, queryset):
        queryset.filter(estado='enviado').update(estado='entregado')
    marcar_entregado.short_description = "Marcar como entregado"