from django.db import models


#Categoria 
class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre


# 2. Talle 
class Talle(models.Model):
    TALLE_CHOICES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    #CharField para almacenar el código XS, S, M
    nombre = models.CharField(max_length=5, choices=TALLE_CHOICES, unique=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Talle'
        verbose_name_plural = 'Talles'

    def __str__(self): 
        return self.get_nombre_display()


class Producto(models.Model):
    GENERO_CHOICES = [
        ('Hombre', 'Hombre'), 
        ('Mujer', 'Mujer'), 
        ('Unisex', 'Unisex')
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    genero = models.CharField(max_length=50, choices=GENERO_CHOICES)
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE)
    
    # Imagen principal del producto
    imagen = models.ImageField(upload_to='productos/principal/', blank=True, null=True)

    def __str__(self):
        return self.nombre

    # calcular el stock total sumando las variantes
    @property
    def stock_total(self):
        return sum(variante.stock for variante in self.variantes.all())

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


# manejar el stock por talle 
class ProductoVariante(models.Model):
    """
    Modelo que relaciona un Producto con un Talle específico
    y rastrea el stock de esa combinación.
    """
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="variantes")
    talle = models.ForeignKey(Talle, on_delete=models.PROTECT) 
    stock = models.PositiveIntegerField(default=0) # Stock específico del talle

    class Meta:
        verbose_name = 'Variante de Producto'
        verbose_name_plural = 'Variantes de Productos'
        unique_together = ('producto', 'talle') 
        
    def __str__(self):
        return f"{self.producto.nombre} - Talle: {self.talle.nombre}"


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
        Producto, on_delete=models.CASCADE, related_name="imagenes")
    imagen = models.ImageField(upload_to="productos/galeria/")

    class Meta:
        verbose_name = 'Imagen de Producto'
        verbose_name_plural = 'Imagenes de Productos'

    def __str__(self):
        return f"Imagen de {self.producto.nombre}"
