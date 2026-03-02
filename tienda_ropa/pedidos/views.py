from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Pedido, ArticuloPedido
from carrito.carrito import Carrito  
from productos.models import Producto 


class HistorialPedidos(LoginRequiredMixin, ListView):
    model = Pedido
    template_name = "pedidos/historial_pedidos.html"
    context_object_name = 'pedidos_usuario' 
    paginate_by = 10 

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by("-creado")


class DetallePedido(LoginRequiredMixin, DetailView):
    model = Pedido
    template_name = "pedidos/detalle_pedidos.html"
    context_object_name = "pedido"

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articulos_pedido'] = self.object.articulos.all()
        return context


def finalizar_compra_view(request):
    if request.method == 'POST':
        
        carrito_sesion = Carrito(request)

        if not carrito_sesion.carrito:
            return redirect('carrito:ver_carrito')
        
        nuevo_pedido = Pedido.objects.create(
            usuario=request.user,  
            monto_total=carrito_sesion.get_total_general() 
        )
        
        for key, item in carrito_sesion.carrito.items():
            
            producto_id = key 
            
            try:
                producto = Producto.objects.get(pk=producto_id)
            except Producto.DoesNotExist:
                continue 
            
            ArticuloPedido.objects.create(
                pedido=nuevo_pedido,        
                producto=producto,
                precio=item['precio'],      
                cantidad=item['cantidad'],
            )

        nuevo_pedido.estado = 'PAGADO'
        nuevo_pedido.pagado = True
        nuevo_pedido.save()

        carrito_sesion.limpiar() 

        return redirect('pedidos:confirmacion_pedido', pedido_id=nuevo_pedido.id)

    return render(request, 'checkout.html')


def confirmacion_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, 'pedidos/confirmacion_pedido.html', {'pedido': pedido})