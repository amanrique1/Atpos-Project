from .models import Producto
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import DatabaseError, OperationalError

def index(request):
    return render(request, 'base.html')

def darProductos(request):
    queryset = Producto.objects.all().order_by('-marca')[:10] #QuerySets para interactuar con el SMBD
    
    #Ejemplo de un QuerySet para cambiar de BD 
    
    # This will run on the 'other' database.
    # Producto.objects.using('otra base de datos definida en DATABASES').all()

    context = {
        'productos_list': queryset
    }    
    return render(request, 'Producto/darProducto.html', context) #Ojo con el HTML

def crearProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()            

            """
            #Ejemplos de .save() en otras BD
            #producto.save(using='la base de datos deseada')
            #Intentar guardar en la base de datos primaria, si no guardar en la local

            try:
                producto.save()
            except (OperationalError, DatabaseError) as excepcion: #Error producido por la mala operacion de la BD principal
                print(str(excepcion)) #Imprimir el error
                producto.save(using='local') #Guardar la informacion en la base de datos local
            """
            
            #Guardar informacion en ambas bases de datos.
            producto.save() #El .save() permite hacer el post en el SMBD
            producto.save(using='local') #Guardar la informacion en la base de datos "local"

            messages.add_message(request, messages.SUCCESS, 'El producto ha sido creado satisfactoriamente')
            return HttpResponse("Producto creado satisfactoriamente")
        else:
            print(form.errors)
    else:
        form = ProductoForm()

    context = {
        'form': form,
    }

    return render(request, 'Producto/crearProducto.html', context)
