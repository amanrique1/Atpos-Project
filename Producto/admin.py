from django.contrib import admin
from .models import Producto, EspecificacionProducto

# Register your models here.

#Se registrara unicamente el modelo de Producto pues es con el cual haremos la prueba
admin.site.register(Producto) #Enlaza el modelo de producto, similar al appmodul de Angular