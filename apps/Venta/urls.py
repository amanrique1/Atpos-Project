from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from apps.Venta.views import *

urlpatterns = [
    url(r'^darFacturas/', darFacturas), #Vista asociada
    url(r'^crearFactura/$', csrf_exempt(crearFactura), name='crearPorducto'),  
    url(r'^darVentas/', darVentas), #Vista asociada
    url(r'^crearVentas/$', csrf_exempt(crearVenta), name='crearEspecificacionProducto'),    
]