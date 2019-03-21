from django.shortcuts import render
from apps.Negocio.models import *
from apps.Producto.models import PuntoDeVentaProds

# Create your views here.
def listarInventario(request,idPVenta):
	
	inventario=PuntoDeVentaProds.objects.all().get(puntoDeVenta_id=idPVenta)
	contexto={'inventario':inventario}
	return render(request, 'Negocio/listarInventario.html',contexto)
