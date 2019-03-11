#Formulario para recaudar datos del usuario
from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:        
        model = Producto #Le dice a Djando que este form es para los modelos de producto
        #Campos a recibir
        fields = ['codigoBarras', 'nombre', 'cantidadMedida', 'unidadMedida', 'descripcion', 'marca']
    


