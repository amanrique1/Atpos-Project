from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from apps.Producto.views import *

urlpatterns = [
    url('^$', index),
    url(r'^darProductos/', darProductos), #Vista asociada
    url(r'^crearProducto/$', csrf_exempt(crearProducto), name='crearPorducto'),  
    url(r'^darEspecificacionesProducto/', darEspecificacacionesProductos), #Vista asociada
    url(r'^crearEspecificacionesProducto/$', csrf_exempt(crearEspecificacionProducto), name='crearEspecificacionProducto'),    
]