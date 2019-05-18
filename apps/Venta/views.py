from django.shortcuts import render
from apps.Venta.models import Factura
from apps.Venta.forms import *
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
import json

#Devuelve todas las facturas.
@api_view(["GET"])
def darFacturas(request):       
    queryset = Factura.objects.all()
    respuesta = [factura.as_json() for factura in queryset]
    return JsonResponse(respuesta, safe=False)

@api_view(["GET"])
def darFacturasUsuario(request, usuario):
    consulta = Factura.objects.filter(usuario=usuario).values()
    return JsonResponse(list(consulta), safe=False)

@api_view(["GET"])
def darFactura(request, id):
    consulta = Factura.objects.get(id=id)
    return JsonResponse(consulta.as_json())

@api_view(["POST"])
def crearFactura(request):    
    if request.method == 'POST':
        datos = JSONParser().parse(request)        
        form = FacturaForm(datos)
        if form.is_valid():
            factura = form.save(commit=False) 
            factura.save()
            respuesta = {"mensaje": "La nueva factura se ha creado satisfactoriamente", "id":factura.id}
            return HttpResponse(json.dumps(respuesta), content_type="application/json", status=200) #Dar Respuesta, json_dumps(dict) convierte un diccionario a texto parecido a stringyfy en JS            
        else:
             respuesta = {"mensaje" : "Existen errores en el proceso de creacion de la factura", "errores" : form.errors}
             return HttpResponse(json.dumps(respuesta), content_type="application/json", status=400) #Dar Respuesta, json_dumps(dict) convierte un diccionario a texto parecido a stringyfy en JS         

@api_view(["POST"])             
def crearVenta(request):    
    if request.method == 'POST':
        datos = JSONParser().parse(request)
        form = VentaForm(datos)
        if form.is_valid():
            venta = form.save(commit=False) 
            venta.save()
            respuesta = {"mensaje": "La venta se ha creado correctamente y asociado a la factura", "id":venta.id}
            return HttpResponse(json.dumps(respuesta), content_type="application/json", status=200) #Dar Respuesta, json_dumps(dict) convierte un diccionario a texto parecido a stringyfy en JS                        
        else:
            respuesta = {"mensaje" : "Existen errores en el proceso de creacion de la factura", "errores" : form.errors}
            return HttpResponse(json.dumps(respuesta), content_type="application/json", status=400) #Dar Respuesta, json_dumps(dict) convierte un diccionario a texto parecido a stringyfy en JS

@api_view(["DELETE"])            
def eliminarVenta(request, factura, especificacionProducto):
    venta = Venta.objects.filter(factura=factura, especificacionProducto=especificacionProducto).get()    
    print("ID Factura: ", factura, " especificacionProducto:", especificacionProducto)
    venta.delete()
    if Venta.objects.filter(factura=factura, especificacionProducto=especificacionProducto).count() == 0:
        respuesta = {"mensaje": "La venta se ha eliminado correctamente y asociado a la factura"}
        return HttpResponse(json.dumps(respuesta), content_type="application/json", status=200) #Dar Respuesta, json_dumps(dict) convierte un diccionario a texto parecido a stringyfy en JS                        
    else:
        respuesta = {"mensaje" : "Existen errores en el proceso de eliminacion de la venta"}
        return HttpResponse(json.dumps(respuesta), content_type="application/json", status=409) #Dar Respuesta, json_dumps(dict) convierte un diccionario a texto parecido a stringyfy en JS
