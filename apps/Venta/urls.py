from django.urls import path
from django.conf.urls import url, include

from apps.Venta.views import *

urlpatterns = [
    url(r'^darFacturas/', darFacturas), #Vista asociada
    url(r'^crearFactura/$', crearFactura, name='crearPorducto'),  
    url(r'^darVentas/', darVentas), #Vista asociada
    url(r'^crearVentas/$', crearVenta, name='crearEspecificacionProducto'),    
]