from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from apps.Negocio.views import *

urlpatterns = [
    url(r'^darInventario/(?P<idPVenta>\d+)$', listarInventario), #Vista asociada  
    url(r'^editarInventario/(?P<idPVenta>\d+)$', actualizarInventario,name='actualizarInventario'), 
    url(r'^crearElementoInventario/', crearElementoInventario), #Vista asociada
    url(r'^darPuntosDeVenta/', listarPuntosDeVenta), #Vista asociada  
    url(r'^crearPuntoDeVenta/', crearPDeVenta), #Vista asociada
]