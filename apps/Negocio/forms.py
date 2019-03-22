from django import forms
from apps.Producto.models import PuntoDeVentaProds
from apps.Negocio.models import PuntoDeVenta

class InventarioForm(forms.ModelForm):
    class Meta:        
        model = PuntoDeVentaProds #Le dice a Djando que este form es para los modelos de producto
        #Campos a recibir
        fields = ['puntoDeVenta', 'especificacionProducto', 'cantidad']
        labels={'puntoDeVenta':'Punto de Venta', 'especificacionProducto':'Especificacion Producto', 'cantidad':'Cantidad'}
        widgets={'puntoDeVenta':forms.Select(attrs={'class':'form-control'}),
                 'especificacionProducto':forms.SelectMultiple(attrs={'class':'form-control'}), 
                 'cantidad':forms.NumberInput(attrs={'class':'form-control'})}

class PuntodeVentaForm(forms.ModelForm):
    class Meta:        
        model = PuntoDeVenta #Le dice a Djando que este form es para los modelos de producto
        #Campos a recibir
        fields = ['nombre', 'ciudad', 'direccion']
        labels={'nombre':'Nombre', 'ciudad':'Ciudad', 'direccion':'Direccion'}
        widgets={'nombre':forms.TextInput(attrs={'class':'form-control'}),
                 'ciudad':forms.TextInput(attrs={'class':'form-control'}), 
                 'direccion':forms.TextInput(attrs={'class':'form-control'})}
