from .models import Producto
from django.shortcuts import render, redirect
from .forms import ProductoForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

def index(request):
    return render(request, 'base.html')

def darProductos(request):
    queryset = Producto.objects.all().order_by('-marca')[:10]
    context = {
        'productos_list': queryset
    }    
    return render(request, 'Producto/darProducto.html', context) #Ojo con el HTML

def crearProducto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save()
            producto.save()
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
