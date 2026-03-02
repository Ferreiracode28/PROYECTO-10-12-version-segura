from .carrito import Carrito

def carrito_context(request):
    return {"carrito": Carrito(request)}