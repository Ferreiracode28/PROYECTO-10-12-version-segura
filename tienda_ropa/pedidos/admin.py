from django.contrib import admin
from . models import Pedido, ArticuloPedido, DireccionEnvio

class ArticuloPedidoInLine(admin.TabularInline):    
    model = ArticuloPedido
    fields = ["producto", "precio", "cantidad"]
    readonly_fields = ["precio"] 
    extra = 0


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'usuario', 
        'estado', 
        'monto_total',
        'direccion_envio', 
        'creado'
        ]
    
    list_filter = ["estado", "pagado", "creado"]
    search_fields = ['usuario__username', 'id', 'direccion_envio__receptor_nombre_completo']
    # Campos que se muesrtan en la página de detalle del Pedido
    fieldsets = [
        ('Información General', {
            'fields': ['usuario', 'estado', 'pagado', 'monto_total'],
        }),
        ('Dirección y Tiempos', {
            'fields': ['creado', 'actualizado', 'direccion_envio'],
        }),
    ]

    # Incluye los artculos del pedido directamente en la página de pedido
    inlines = [ArticuloPedidoInLine]
    
    # Campos solo lectura
    readonly_fields = ['monto_total', 'creado', 'actualizado']


@admin.register(DireccionEnvio)
class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = [
        'receptor_nombre_completo', 
        'direccion', 
        'ciudad', 
        'pais', 
        'usuario'
    ]
    search_fields = ['receptor_nombre_completo', 'direccion', 'ciudad']
    list_filter = ['pais', 'usuario']