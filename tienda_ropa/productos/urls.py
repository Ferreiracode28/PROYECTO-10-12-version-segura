from django.urls import path
from .views import ListaProductosView, DetalleProductoView, ListaPorCategoriaView


app_name = 'rustikal'

urlpatterns = [
   
    path('', ListaProductosView.as_view(), name='lista'),
    path('categoria/<str:categoria_nombre>/', ListaPorCategoriaView.as_view(), name='lista_por_categoria'),
    path('<int:pk>/<str:nombre>/', DetalleProductoView.as_view(), name='detalle'),
]