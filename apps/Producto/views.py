from django.shortcuts import render, redirect
from apps.Producto.forms import ProductoForm,EspecificacionProductoForm
from apps.Producto.models import *

#Variables globales

#Indica un semaforo mutex para una seccion de exclusion mutua, se usa para tener cuidado de no crear
#varios threads para migrar la informacion, solo uno

def index(request):
    return render(request, 'Producto/base.html')

def darProductos(request):
       
    queryset = Producto.objects.all().order_by('-marca')[:10] #QuerySets para interactuar con el SMBD
   
    #Ejemplo de un QuerySet para cambiar de BD 
    
    # This will run on the 'other' database.
    # Producto.objects.using('otra base de datos definida en DATABASES').all()

    context = {
        'productos_list': queryset
    }

    return render(request, 'Producto/darProducto.html', context) #Ojo con el HTML

def darEspecificacacionesProductos(request):
    
    queryset = EspecificacionProducto.objects.all()[:10] #QuerySets para interactuar con el SMBD
   
    
    #Ejemplo de un QuerySet para cambiar de BD 
    
    # This will run on the 'other' database.
    # Producto.objects.using('otra base de datos definida en DATABASES').all()

    context = {
        'espList': queryset
    }

    return render(request, 'Producto/darEspecificacionesProducto.html', context) #Ojo con el HTML

def crearProducto(request):
    
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False) #Traer solo el valor de objeto form
           
            #Ejemplos de .save() en otras BD
            #producto.save(using='la base de datos deseada')
            #Intentar guardar en la base de datos primaria, si no guardar en la local
            producto.save()
            return redirect('../darProductos')
        else:
            print(form.errors)
    else:
        form = ProductoForm()

    context = {
        'form': form,
    }

    return render(request, 'Producto/crearProducto.html', context)

def crearEspecificacionProducto(request):
    if request.method == 'POST':
        form = EspecificacionProductoForm(request.POST)
        if form.is_valid():
            espProd = form.save(commit=False) #Traer solo el valor de objeto form
           
            #Ejemplos de .save() en otras BD
            #producto.save(using='la base de datos deseada')
            #Intentar guardar en la base de datos primaria, si no guardar en la local
            
            espProd.save()
            
           
            return redirect('../darEspecificacionProducto')
        else:
            print(form.errors)
    else:
        form = EspecificacionProductoForm()

    context = {
        'form': form,
    }

    return render(request, 'Producto/crearEspecificacionProducto.html', context)





