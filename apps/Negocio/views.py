from django.shortcuts import render,redirect
from apps.Negocio.models import *
from apps.Producto.models import PuntoDeVentaProds
from apps.Negocio.forms import *

# Create your views here.
def listarInventario(request,idPVenta):
	
	inventario=PuntoDeVentaProds.objects.all().get(puntoDeVenta_id=idPVenta)
	contexto={'inventario':inventario}
	return render(request, 'Negocio/listarInventario.html',contexto)

def actualizarInventario(request,idPVenta):

	inventario=PuntoDeVentaProds.objects.get(puntoDeVenta_id=idPVenta)
	if request.method=='GET':
		form=InventarioForm(instance=inventario)
	else:
		form=InventarioForm(request.POST,instance=inventario)
		if form.is_valid():
			form.save()
		return redirect('../darInventario/'+idPVenta)
	return render(request,'Negocio/inventarioForm.html',{'formu':form})

def crearElementoInventario(request):
	if request.method =='POST':
		form=InventarioForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('../darPuntosDeVenta')

	else:
		form=InventarioForm()

	return render(request,'Negocio/inventarioForm.html',{'form':form})

def listarPuntosDeVenta(request):
	
	puntos=PuntoDeVenta.objects.all()
	contexto={'puntos':puntos}
	return render(request, 'Negocio/listarPDeVenta.html',contexto)

def crearPDeVenta(request):
	if request.method =='POST':
		form=PuntodeVentaForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('../darPuntosDeVenta')

	else:
		form=PuntodeVentaForm()

	return render(request,'Negocio/puntoDeVentaForm.html',{'form':form})
