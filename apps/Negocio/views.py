from django.shortcuts import render
from apps.Negocio.models import *

# Create your views here.
def listarInventario(request,idPVenta):
	
	inventario=PuntoDeVentaProds.objects.all().get(puntoDeVenta=idPVenta)
	contexto={'inventario':inventario}
	return render(request, 'Negocio/listarInventario.html',contexto)
