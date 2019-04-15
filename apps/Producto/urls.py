from django.urls import path
from django.conf.urls import url, include

from apps.Producto.views import *

urlpatterns = [
    url('^$', index),
    url(r'^darProductos/', darProductos), #Vista asociada
    url(r'^crearProducto/$', crearProducto, name='crearPorducto'),  
    url(r'^darEspecificacionesProducto/', darEspecificacacionesProductos), #Vista asociada
    url(r'^crearEspecificacionesProducto/$', crearEspecificacionProducto, name='crearEspecificacionProducto'),
    url(r'^darInventario/', darEspecificacacionesProductos), #Vista asociada
    url(r'^crearInventario/$',crearInventario, name='crearEspecificacionProducto'),        
]