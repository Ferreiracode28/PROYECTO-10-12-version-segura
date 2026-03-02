from django.db import models
from django.conf import settings
from productos.models import Producto

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Pedido(models.Model):
    ESTADOS_CHOICES = [
        ('PENDIENTE', 'Pendiente de Pago'),
        ('PAGADO', 'Pagado / En Procesamiento'),
        ('ENVIADO', 'Enviado'),
        ('ENTREGADO', 'Entregado'),
        ('CANCELADO', 'Cancelado'),]
    
    usuario = models.ForeignKey(AUTH_USER_MODEL, related_name= "pedidos", on_delete= models.CASCADE, verbose_name= 'Cliente')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=100, choices= ESTADOS_CHOICES, default= 'PENDIENTE')
    pagado = models.BooleanField(default=False) #Indicador de pago realziado, para evitar refacturaciones
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    direccion_envio = models.ForeignKey(
    'DireccionEnvio', related_name='pedidos_por_direccion', on_delete=models.SET_NULL, null=True,blank=True, verbose_name='Dirección de Envío del Pedido')

    class Meta:
        ordering = ['-creado']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'

    def __str__(self):
        return f'Pedido {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.articulos.all())
    


class DireccionEnvio(models.Model):
    usuario = models.ForeignKey(
        AUTH_USER_MODEL,
        related_name='direcciones_guardadas',
        on_delete=models.SET_NULL, # Si el usuario se elimina, la dirección no lo hace.
        null=True,
        blank=True
    )
    receptor_nombre_completo = models.CharField(max_length=150, verbose_name='Receptor')
    direccion = models.CharField(max_length=250, verbose_name='Dirección')
    ciudad = models.CharField(max_length=100, verbose_name='Ciudad')
    codigo_postal = models.CharField(max_length=20, verbose_name='Código Postal')
    pais = models.CharField(max_length=100, verbose_name='País')

    class Meta:
        verbose_name = 'Dirección de Envío'
        verbose_name_plural = 'Direcciones de Envío'
    
    def __str__(self):
        return f"{self.direccion}, {self.ciudad} ({self.codigo_postal})"
    
class ArticuloPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name= "articulos", on_delete= models.CASCADE)
    producto = models.ForeignKey(Producto, related_name= "articulos_pedidos", on_delete= models.CASCADE)
    precio = models.DecimalField(max_digits=10, decimal_places=2) #Para el historial
    cantidad = models.PositiveBigIntegerField(default=1)

    class Meta:
        verbose_name = "articulo de pedido"
        verbose_name_plural = "articulos de pedidos"

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        #Calcula el costo total de esta línea de artículo (precio * cantidad).
        return self.precio * self.cantidad
