from django.urls import path
from . import views

app_name = 'pedidos' 

urlpatterns = [
    path('historial/', views.HistorialPedidos.as_view(), name='historial'),
    path('detalle/<int:pk>/', views.DetallePedido.as_view(), name='detalle'),
    path('finalizar-compra/', views.finalizar_compra_view, name='finalizar_compra'),
    path('confirmacion/<int:pedido_id>/', views.confirmacion_pedido_view, name='confirmacion_pedido'),
]