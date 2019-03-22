from django.shortcuts import render
from apps.Venta.models import Factura
from apps.Venta.forms import *

# Create your views here.
def darFacturas(request):
       
    queryset = Factura.objects.all()[:10] #QuerySets para interactuar con el SMBD
   
    #Ejemplo de un QuerySet para cambiar de BD 
    
    # This will run on the 'other' database.
    # Producto.objects.using('otra base de datos definida en DATABASES').all()

    context = {
        'facturas': queryset
    }

    return render(request, 'Venta/listarFacturas.html', context) #Ojo con el HTML
def crearFactura(request):
    
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save(commit=False) 
            factura.save()
            #return redirect('../darProductos')
        else:
            print(form.errors)
    else:
        form = FacturaForm()

    context = {
        'form': form,
    }

    return render(request, 'Venta/facturaForm.html', context)

def darVentas(request):
       
    queryset = Venta.objects.all()[:10] #QuerySets para interactuar con el SMBD
   
    #Ejemplo de un QuerySet para cambiar de BD 
    
    # This will run on the 'other' database.
    # Producto.objects.using('otra base de datos definida en DATABASES').all()

    context = {
        'ventas': queryset
    }

    return render(request, 'Venta/listarVentas.html', context) #Ojo con el HTML
def crearVenta(request):
    
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False) 
            venta.save()
            return redirect('../darProductos')
        else:
            print(form.errors)
    else:
        form = VentaForm()

    context = {
        'form': form,
    }

    return render(request, 'Venta/ventaForm.html', context)
