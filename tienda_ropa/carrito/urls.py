from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('', views.ver_carrito, name='ver_carrito'), 
   path('agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('eliminar/<int:producto_id>/', views.eliminar, name='eliminar_carrito'),
    path('sumar/<int:producto_id>/', views.sumar, name='sumar_carrito'),
    path('restar/<int:producto_id>/', views.restar, name='restar_carrito'),
]
