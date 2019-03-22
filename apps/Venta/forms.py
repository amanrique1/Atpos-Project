#Formulario para recaudar datos del usuario
from django import forms
from apps.Venta.models import *

class FacturaForm(forms.ModelForm):
    class Meta:        
        model = Factura #Le dice a Djando que este form es para los modelos de factura
        #Campos a recibir
        fields = ['fecha', 'metodoDePago', 'pagado']
        labels={'fecha':'Fecha', 'metodoDePago':'Metodo de pago', 'pagado':'Pagado'}
        widgets={'fecha':forms.DateInput(attrs={'class':'form-control'}),  
                 'metodoDePago':forms.TextInput(attrs={'class':'form-control'}),
                 'pagado':forms.NullBooleanSelect(attrs={'class':'form-control'})}

class VentaForm(forms.ModelForm):
    class Meta:        
        model = Venta #Le dice a Djando que este form es para los modelos de producto
        #Campos a recibir
        fields = ['especificacionProducto', 'factura', 'cantidad']
        labels={'especificacionProducto':'Especificacion Producto', 'factura':'Factura', 'cantidad':'Cantidad'}
        widgets={'especificacionProducto':forms.Select(attrs={'class':'form-control'}), 
                 'factura':forms.SelectMultiple(attrs={'class':'form-control'}), 
                 'cantidad':forms.NumberInput(attrs={'class':'form-control'})}
    


