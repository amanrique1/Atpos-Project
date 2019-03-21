from apps.models import Producto,EspecificacionProducto
from django.shortcuts import render, redirect
from apps.Producto.forms import ProductoForm,EspecificacionProductoForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import DatabaseError, OperationalError, connections
from threading import Thread, Lock, Event
from .serializers import ProductoSerializer

#Variables globales

#Indica un semaforo mutex para una seccion de exclusion mutua, se usa para tener cuidado de no crear
#varios threads para migrar la informacion, solo uno

mutex = Lock() #Solicitar mutex
migrando = False #Indica si hay o no Threads trabajando en migracion de datos
evento_wait = Event() #Solicitar un nuevo evento para encolar los thread que hagan wait() y poder hacer notify()


def index(request):
    return render(request, 'base.html')

def darProductos(request):
    verificarMigracion('default', 'local', Producto) #Realizar verificacion de la DB local para migracion

    queryset = None #Inicializar variable

    if verificarConexion('default'):
        queryset = Producto.objects.all().order_by('-marca')[:10] #QuerySets para interactuar con el SMBD
    else:
        queryset = Producto.objects.using('local').all().order_by('-marca')[:10] #QuerySets para interactuar con el SMBD
    
    #Ejemplo de un QuerySet para cambiar de BD 
    
    # This will run on the 'other' database.
    # Producto.objects.using('otra base de datos definida en DATABASES').all()

    context = {
        'productos_list': queryset
    }

    return render(request, 'Producto/darProducto.html', context) #Ojo con el HTML

def crearProducto(request):
    verificarMigracion('default', 'local', Producto) #Realizar verificacion de la DB local para migracion

    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = form.save(commit=False) #Traer solo el valor de objeto form
           
            #Ejemplos de .save() en otras BD
            #producto.save(using='la base de datos deseada')
            #Intentar guardar en la base de datos primaria, si no guardar en la local
            try:
                producto.save()
            except (OperationalError, DatabaseError) as excepcion: #Error producido por la mala operacion de la BD principal
                print("Se ha perdido la conexion a la base de datos global, cambiando a sistema auxiliar")
                # print(str(excepcion)) Imprimir el error
                producto.save(using='local') #Guardar la informacion en la base de datos local                        
            
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

def crearEspecificacionProducto(request):
    verificarMigracion('default', 'local', Producto) #Realizar verificacion de la DB local para migracion

    if request.method == 'POST':
        form = EspecificacionProductoForm(request.POST)
        if form.is_valid():
            espProd = form.save(commit=False) #Traer solo el valor de objeto form
           
            #Ejemplos de .save() en otras BD
            #producto.save(using='la base de datos deseada')
            #Intentar guardar en la base de datos primaria, si no guardar en la local
            try:
                espProd.save()
            except (OperationalError, DatabaseError) as excepcion: #Error producido por la mala operacion de la BD principal
                print("Se ha perdido la conexion a la base de datos global, cambiando a sistema auxiliar")
                # print(str(excepcion)) Imprimir el error
                espProd.save(using='local') #Guardar la informacion en la base de datos local                        
            
            messages.add_message(request, messages.SUCCESS, 'El producto ha sido creado satisfactoriamente')
            return HttpResponse("Producto creado satisfactoriamente")
        else:
            print(form.errors)
    else:
        form = ProductoForm()

    context = {
        'form': form,
    }

    return render(request, 'Producto/crearEspecificacionProducto.html', context)

def migrarDBlocal(model):

    global migrando #Hacer referencia a la variable global "migrando"  
    
    #Construir un QuerySet para recorrer todos los valores presentes en la DB local
    querySet = model.objects.using('local').all() #Traer todos los valores a migrar
    
    #Variable para listar
    i = 0   

    for registro in querySet:
        try:
            i += 1
            dict_data = ProductoSerializer(registro).data
            print("\n ===== Migracion a la base de datos global ======= \n")
            print(str(i) + "). " + imprimirValores(dict_data))        
            print("Almacenando registro en la base de datos global")
            registro.save(using='default')
            #Borrar el registro de la base de datos local
            registro.delete(using='local') #Ojo que el parametro using indica la DB donde se ejecuta la operacion        
            print("Registro borrado de la base de datos local")
            print("=============================================== \n")
            
        except (OperationalError, DatabaseError) as excepcion:            
            print("[Migrar DB Local] La conexion a la base de datos ha fallado, esperando reconexion")
            evento_wait.wait()    

    #Terminacion exitosa
    print("[Migrar DB Local] La migracion para los datos del modelo ha sido exitosa")
    mutex.acquire()
    migrando = False
    if migrando is not False:
        print("[Migrar DB Local] Error faltal de candados")
    mutex.release()

#Devuelve una cadena de texto con los datos del dicccionario
def imprimirValores(diccionario):
    cadena_respuesta = ""
    for key,value in diccionario.items():
        cAux = str(key) + " : " + str(value) + "\n"
        cadena_respuesta += cAux
    return cadena_respuesta

#Verifica si hay conexion al servidor central, en caso de que la haya migrar la base de datos auxiliar
def verificarMigracion(idDB, idDBLocal, model):

    if model.objects.using(idDBLocal).count() == 0:
        print("[Verificar-Migracion] La base de datos auxiliar no tiene registros sobre el modelo") 
        return None   
    
    global migrando #Hacer referencia a la variable global "migrando"
    hay_conexion = verificarConexion(idDB)
    
    if hay_conexion:        
        #Exclusion mutua - consultar si hay threads migrando
        evento_wait.set() #Despertar al thread de migracion si se durmio porque hubo un error (Hacer notify())
        mutex.acquire()       
        if migrando == True:
            #Liberar recurso y terminar - ya hay alguien haciendo el proceso
            print("[Verificar-Migracion] Ya se encuentra en progreso el proceso de migracion")
            mutex.release()
            return None
        else: #No hay nadie migrando -  cambiar estado y comenzar a migrar
            migrando = True
            mutex.release() #Liberar candado
            print("[Verificar-Migracion] Lanzando proceso de migracion")
            nuevoHilo = Thread(name="Geovanny", target=migrarDBlocal, args=(model,)) #Objeto
            nuevoHilo.start()
    
# Permite verificar la conexion a una DB existente
# @param idDB - Es el identificador de la base de datos que se desea verificar conexion
# return True si hay conexion a la base de datos deseada, False de lo contrario

def verificarConexion(idDB):
    
    #Declarar cursor para conexion a la DB
    enlace = connections[idDB] #Default es la DB Global
    hay_conexion = False

    #Conectar y obtener cursor
    try:
       cursor = enlace.cursor()
    except (OperationalError, DatabaseError) as excepcion:
        print("[Verificar-Conexion] La conexion a la base de datos " + idDB + " ha fallado",)
    else:
        #Conexion exitosa
        hay_conexion = True        
        cursor.close()

    return hay_conexion
    
        




