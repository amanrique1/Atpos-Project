from django.urls import path
from django.conf.urls import url, include

from apps.Venta.views import *

urlpatterns = [
    url(r'^darfacturas/', darFacturas), #Vista asociada
    url(r'^darfacturasusuario/(?P<usuario>[\w\-]+)$', darFacturasUsuario),
    url(r'^darfactura/(?P<id>\d+)$', darFactura),    
    url(r'^crearventa/$', crearVenta),
    url(r'^crearfactura/$', crearFactura),    
    url(r'^eliminarventa/(?P<factura>\d+)/venta/(?P<especificacionProducto>[\w\-]+)$', eliminarVenta)    
]