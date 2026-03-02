from django.shortcuts import redirect, render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .carrito import Carrito
from productos.models import Producto


def ver_carrito(request):
    carrito = Carrito(request)
    return render(request, "carrito/ver_carrito.html", {
        "carrito": carrito
    })

def agregar_carrito(request, producto_id):
    carrito = Carrito(request)
    
    cantidad = 1
    if request.method == 'POST':
        try:
            cantidad = int(request.POST.get('cantidad', 1))
        except ValueError:
            cantidad = 1

    carrito.agregar(producto_id, cantidad=cantidad)
    
    referring_url = request.META.get('HTTP_REFERER')
    
    if referring_url:
        if '?' in referring_url:
            return redirect(f"{referring_url}&cart_open=true")
        else:
            return redirect(f"{referring_url}?cart_open=true")
    
    return redirect(reverse('rustikal:lista'))

def restar(request, producto_id):
    carrito = Carrito(request)
    carrito.restar(producto_id)
    return redirect("carrito:ver_carrito") 

def sumar(request, producto_id):
    carrito = Carrito(request)
    carrito.agregar(producto_id, cantidad=1) 
    return redirect("carrito:ver_carrito") 

def eliminar(request, producto_id):
    carrito = Carrito(request)
    
    if request.method == 'POST':
        # Maneja la petición del sidebar
        carrito.eliminar(producto_id)
        return JsonResponse({'status': 'ok'})

    # Maneja la petición del botón en la página principal
    carrito.eliminar(producto_id)
    return redirect("carrito:ver_carrito")