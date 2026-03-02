from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
# Importante para proteger la vista
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UsuarioPersonalizado
from .forms import PerfilForm, EdicionPerfilForm
from django.contrib import messages # Importamos messages para feedback



class RegistroPerfil(CreateView):
    model = UsuarioPersonalizado
    form_class = PerfilForm
    template_name = 'usuarios/registro.html'
    success_url = success_url = '/usuarios/login/'


class EdicionPerfil(LoginRequiredMixin, UpdateView):
    model = UsuarioPersonalizado
    form_class = EdicionPerfilForm
    template_name = 'usuarios/edicion_perfil.html'
    
    # CORRECCIÓN: Redirigimos a la lista principal de productos (rustikal:lista)
    success_url = reverse_lazy('rustikal:lista') 
    
    def form_valid(self, form):
        # Agregamos un mensaje de éxito después de guardar
        messages.success(self.request, "¡Tu perfil ha sido actualizado exitosamente!")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        # Devuelve el usuario actual para que pueda editar su propio perfil
        return self.request.user