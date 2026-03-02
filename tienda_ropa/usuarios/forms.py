from django import forms
from .models import UsuarioPersonalizado
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput, EmailInput # Importamos widgets básicos


class PerfilForm(UserCreationForm):
    # Hacer que el email sea requerido en el registro
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = UsuarioPersonalizado
        # Incluir todos los campos necesarios para el registro
        fields = UserCreationForm.Meta.fields + \
            ('email', 'nro_telefono', 'avatar')
        
        # Asignamos el widget TextInput y la clase 'form-style' a los campos de texto
        widgets = {
            'email': EmailInput(attrs={'class': 'form-style'}),
            'username': TextInput(attrs={'class': 'form-style'}),
            'nro_telefono': TextInput(attrs={'class': 'form-style'}),
            # Las contraseñas (password1/2) se manejan por defecto por UserCreationForm
        }


class EdicionPerfilForm(UserChangeForm):
    # ELIMINAMOS la redefinición manual del campo nro_telefono
    
    password = None  # Excluir el campo de contraseña del Formulario (Correcto)

    class Meta:
        model = UsuarioPersonalizado
        # Incluir solo los campos editables
        fields = ['username', 'email', 'nro_telefono', 'avatar']
        
        # Asignamos el widget TextInput y la clase 'form-style'
        widgets = {
            'username': TextInput(attrs={'class': 'form-style'}),
            'email': EmailInput(attrs={'class': 'form-style'}),
            'nro_telefono': TextInput(attrs={'class': 'form-style'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Eliminamos el campo de contraseña (ya excluido por password=None)
        if 'password' in self.fields:
            del self.fields['password']
            
        # Eliminar campos internos y de seguridad que UserChangeForm añade por defecto
        for fieldname in ['last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions']:
            if fieldname in self.fields:
                del self.fields[fieldname]