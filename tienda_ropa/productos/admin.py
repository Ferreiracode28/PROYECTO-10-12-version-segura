from django.contrib import admin
from .models import Producto, Categoria, Talle, ProductoVariante, ProductoImagen


# FORMULARIOS ANIDADOS EN LA PAG DEL PRODUCTO

class ProductoVarianteInline(admin.TabularInline):
    """Permite la edición de tallas y stock directamente en el Producto."""
    model = ProductoVariante
    extra = 0  # No muestra filas vacías por defecto
    # La clave de esto es que en la misma fila puedes seleccionar Talle y definir Stock
    list_display = ('talle', 'stock')

class ProductoImagenInline(admin.TabularInline):
    """Permite la edición y subida de imágenes de galería en el Producto."""
    model = ProductoImagen
    extra = 0


# REGISTRO PRINCIPAL DE PRODUCTO


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    """Configuración del panel de administración para el modelo Producto."""
    
    # Campos que se muestran en la lista de productos
    list_display = ('nombre', 'get_total_stock', 'precio', 'genero', 'categoria')
    
    # Filtros laterales
    list_filter = ('genero', 'categoria')
    
    # Campos para la barra de búsqueda
    search_fields = ('nombre', 'descripcion')
    
    inlines = [ProductoVarianteInline, ProductoImagenInline]
    
    # Eliminamos el campo talles del modleo lo excluimos si existiera para evitar conflictos
    exclude = ('talles',)
    
    def get_total_stock(self, obj):
        """Calcula el stock total sumando el stock de todas sus variantes."""
       
        return sum(variante.stock for variante in obj.variantes.all())
    
    get_total_stock.short_description = 'Stock Total'


#MODELOS AUXILIARES

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',) 