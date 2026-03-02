from django.views.generic import ListView, DetailView
from .models import Producto, Categoria, ProductoVariante
from django.shortcuts import get_object_or_404

# home de la sección de productos
class ListaProductosView(ListView):
    model = Producto
    template_name = 'productos/lista_productos.html' 
    context_object_name = 'productos'
    paginate_by = 12  # Paginacion 

    def get_queryset(self):
        queryset = super().get_queryset()
        
        genero = self.request.GET.get('genero')
        if genero in ['Hombre', 'Mujer', 'Unisex']:
            queryset = queryset.filter(genero=genero)
            
        return queryset.prefetch_related('variantes', 'imagenes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todas_categorias'] = Categoria.objects.all()
        context['titulo_pagina'] = "Todos los Productos"
        return context


class ListaPorCategoriaView(ListView):
    model = Producto
    template_name = 'productos/lista_productos.html' 
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        categoria_nombre = self.kwargs['categoria_nombre']  
        
        self.categoria = get_object_or_404(Categoria, nombre__iexact=categoria_nombre)
        
        queryset = Producto.objects.filter(categoria=self.categoria).prefetch_related('variantes', 'imagenes')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Productos en {self.categoria.nombre}"
        context['todas_categorias'] = Categoria.objects.all()
        return context


# Vista para mostrar los detalles de un solo producto
class DetalleProductoView(DetailView):
    model = Producto
    template_name = 'productos/detalle_producto.html'
    context_object_name = 'producto' 

    def get_queryset(self):
        return Producto.objects.prefetch_related(
            'variantes__talle', 
            'imagenes'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenemos solo las varientes talles que tienen stock > 0
        variantes_disponibles = self.object.variantes.filter(stock__gt=0).order_by('talle__nombre')
        context['variantes_disponibles'] = variantes_disponibles
        
        return context
