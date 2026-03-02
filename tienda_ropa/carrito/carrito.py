from productos.models import Producto

class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        carrito = self.session.get("carrito")
        if not carrito:
            carrito = self.session["carrito"] = {}

        self.carrito = carrito

    def agregar(self, producto_id, cantidad=1):
        producto = Producto.objects.get(id=producto_id)

        producto_id = str(producto.id)

        if producto_id not in self.carrito:
            self.carrito[producto_id] = {
                "producto_id": producto.id, 
                "nombre": producto.nombre,
                "precio": float(producto.precio),
                "cantidad": cantidad,
                "imagen_url": producto.imagen.url if producto.imagen else None 
            }
        else:
            self.carrito[producto_id]["cantidad"] += cantidad

        self.guardar()

    def eliminar(self, producto_id):
        producto_id = str(producto_id)

        if producto_id in self.carrito:
            del self.carrito[producto_id]

        self.guardar()

    def restar(self, producto_id):
        producto_id = str(producto_id)

        if self.carrito[producto_id]["cantidad"] > 1:
            self.carrito[producto_id]["cantidad"] -= 1
        else:
            del self.carrito[producto_id]

        self.guardar()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session.modified = True

    def guardar(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    @property
    def items(self):
        """
        Genera una lista para el template
        con subtotal por producto, incluyendo la URL de la imagen.
        """
        items = []
        for id_producto, datos in self.carrito.items():
            subtotal = datos["precio"] * datos["cantidad"]
            items.append({
                "id": id_producto,
                "nombre": datos["nombre"],
                "precio": datos["precio"],
                "cantidad": datos["cantidad"],
                "subtotal": subtotal,
                "imagen_url": datos.get("imagen_url"), # AGREGADO
            })
        return items

    @property
    def total(self):
        return sum(item["subtotal"] for item in self.items)
    
    def get_total_general(self):
        """
        Retorna el total del carrito. Utilizado por la vista de Pedidos.
        """
        return self.total
    
    def __len__(self):
        """
        Cuenta el número total de ítems, útil para el ícono del carrito.
        """
        return sum(item['cantidad'] for item in self.carrito.values())