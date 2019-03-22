#Formulario para recaudar datos del usuario
from django import forms
from apps.Producto.models import Producto, EspecificacionProducto, Inventario

class ProductoForm(forms.ModelForm):
    class Meta:        
        model = Producto #Le dice a Djando que este form es para los modelos de producto
        #Campos a recibir
        fields = ['codigoBarras', 'nombre', 'cantidadMedida', 'unidadMedida', 'descripcion', 'marca']
        labels={'codigoBarras':'Codigo de Barras', 'nombre':'Nombre', 'cantidadMedida':'Cantidad Medida', 'unidadMedida':'Unidad Medida', 'descripcion':'Descripcion', 'marca':'Marca'}
        widgets={'codigoBarras':forms.TextInput(attrs={'class':'form-control'}),
        	    'nombre':forms.TextInput(attrs={'class':'form-control'}),
        	    'cantidadMedida':forms.NumberInput(attrs={'class':'form-control'}), 
        	    'unidadMedida':forms.TextInput(attrs={'class':'form-control'}),
        	    'descripcion':forms.TextInput(attrs={'class':'form-control'}), 
        	    'marca':forms.TextInput(attrs={'class':'form-control'})}

class EspecificacionProductoForm(forms.ModelForm):
    class Meta:        
        model = EspecificacionProducto #Le dice a Djando que este form es para los modelos de producto
        #Campos a recibir
        fields = ['idEspecificacionProducto', 'precio', 'precioUnidadMedida', 'fechaVencimiento', 'producto', 'puntoDeVenta']
        labels={'idEspecificacionProducto':'Id EspecificacionProducto', 'precio':'Precio', 'precioUnidadMedida':'Precio Unidad Medida', 'fechaVencimiento':'Fecha Vencimiento', 'producto':'Producto', 'puntoDeVenta':'Punto de Venta'}
        widgets={'idEspecificacionProducto':forms.TextInput(attrs={'class':'form-control'}),
                'precio':forms.TextInput(attrs={'class':'form-control'}),
                'precioUnidadMedida':forms.NumberInput(attrs={'class':'form-control'}), 
                'fechaVencimiento':forms.DateInput(attrs={'class':'form-control'}), 
                'producto':forms.Select(attrs={'class':'form-control'}),
                'puntoDeVenta':forms.Select(attrs={'class':'form-control'})}
    

class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = ['especificacionProducto', 'cantidad']