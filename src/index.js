//Sección de librerias, el requiere indica que al ejecutar se necesita el paquete en especifico
const express = require('express')
const app = express() //Invoca las funciones de la libreria express para su posterior uso.
const PUERTO = 3000 //Puerto de ejecucion
const bodyParser = require('body-parser') //Parser para el cuerpo de las peticiones
const MongoClient = require('mongodb').MongoClient; //API para conexiones en MongoDB

//Configura el parser para formato JSON
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); // support json encoded bodies

//Configuracion de MongoDB
const uri = "mongodb+srv://Spectra:$Spectra09$@microservicio-negocio-jkqvg.mongodb.net/test?retryWrites=true";
const client = new MongoClient(uri, {useNewUrlParser:true});
var db; //Referencia a la base de datos.

//Diccionario con las rutas de los recursos del microservicio
const rutas = {
    "crearpunto" : "/crearpunto",
    "darpuntociudad": "/darpuntociudad/ciudad/:ciudad/direccion/:direccion",
    "actualizarpunto": "/actualizarpunto/ciudad/:ciudad/direccion/:direccion",
    "eliminarpunto": "/eliminarpunto/ciudad/:ciudad/direccion/:direccion",
    "darpuntos": "/darpuntos",
    "darpuntonombre": "/darpuntonombre/:nombre"
}

//Etiquetas para el formato del json con los datos.
const formato = ["nombre", "ciudad", "direccion"]

//Configura el puerto de despliegue de la aplicacion, el siguiente parametro es una funcion
//con la que esperamos recibir parametros y ejecutar.
//En primer lugar haremos la conexion con MongoDB, si es correcta, lanzamos la aplicacion

client.connect(err => {
    if (err) return console.log(err) //Muestra el error en consola en caso de presentarse
    db = client.db("test") //Nombre de la base de datos por defecto.
    app.listen(PUERTO, function(){ //Realizar el despligue y poner en funcionamiento
        console.log(`Prueba correcta en el puerto ${PUERTO}`)
    });
});

//Permite confirmar que el cuerpo de la peticion posee todos los valores solicitados para hacer un post
function confirmarCuerpo(datos) {
    camposFaltantes = {} //Diccionario para responder los campos que faltan     
    if (Object.keys(datos).length === 0) return false    
    for(const clave of formato) {        
        if(datos[clave] === null || typeof datos[clave] != 'string') {
            camposFaltantes[clave] = "El valor no existe o no esta dado en el formato correcto (string)"
        }
    }   
    
    return Object.keys(camposFaltantes).length != 0 ? camposFaltantes : true
}

//Mensaje raiz para el indice
app.get('/', (request, response) => {
    let ruta = JSON.stringify(rutas) //Acceso a variable global
    let mensaje = "Bienvenido al microservicio de puntos de venta del negocio, rutas disponibles \n\n"    
    response.send(mensaje.concat(ruta))    
});

//Operaciones CRUD.

//POST: Crear un nuevo punto de venta para el negocio
app.post(rutas["crearpunto"], (request, response) => {
    console.log(request.body)
    confirmado = confirmarCuerpo(request.body)
    if (confirmado === false) { //El cuerpo de la peticion llego vacio
        mensaje = {"mensaje": "El cuerpo del mensaje está vacio"}
        response.status(400).send(mensaje)
    }
    else if (confirmado === true) { //El cuerpo es correcto
        const colleccion = db.collection('puntos') //Nombre del documento donde guardaremos la informacion
        colleccion.insertOne(request.body, (error, resultado) => {
            if (error) { //Informar errores al usuario
                console.log(error)
                mensaje = {"mensaje": "Se presentaron errores guardando el valor en la base de datos"}
                response.status(500).send(mensaje)
            }
            response.send({"mensaje":"Punto creado satisfactoriamente"})
        });
    }    
    else { //El cuerpo no es correcto hay errores
        response.status(400).send(confirmado)
    }
});

//GET: Obtener la informacion de todos los puntos de venta del negocio
app.get(rutas["darpuntos"], (request, response) =>{
    const cursor = db.collection('puntos').find() //Da un cursor para recorrer todos los registros de la collecion
    const puntos = cursor.toArray((error, resultado) =>{
        response.send(resultado) //Enviar el resultado
    });
});

//GET: Obtener la informacion de un punto de venta en el negocio dada la ciudad y la direccion.
app.get(rutas["darpuntociudad"], (request, response) => {
    
    //Las consultas para MongoDB se realizan mediante BSON, la sintaxis del Query es un diccionario
    query = {
        $and: [ //$and indica que todos los criterios consecutivos iran bajo la clausula del Y
            {ciudad: request.params.ciudad}, //Criterio equals ($eq)
            {direccion: request.params.direccion}
        ]
    }
    
    db.collection('puntos').findOne(query, function(err, result){
        if (result != null) { //Si la consulta arrojo algun resultado y no es vacia
        console.log(`Nombre: ${result.nombre} Direccion: ${result.direccion}`)
        mensaje = {"_id": result._id,"nombre": result.nombre, "direccion": result.direccion, "ciudad": result.ciudad}
        return response.send(mensaje)        
        }
        
        return response.status(404).send({"mensaje": "No se ha encontrado el punto de venta, recuerde que los valores de entrada deben ser exactos"}) //La consulta ha sido vacia
    })
});   

//GET: Obtener la informacion de un punto de venta en el negocio dada la ciudad y la direccion.
app.get(rutas["darpuntonombre"], (request, response) => {

    //Las consultas para MongoDB se realizan mediante BSON, la sintaxis del Query es un diccionario
    query = {
        $and: [ //$and indica que todos los criterios consecutivos iran bajo la clausula del Y
            {nombre: request.params.nombre}, //Criterio equals ($eq)            
        ]
    }
    
    //Ejecuta la consulta y devuelve los datos de interes.    
    db.collection('puntos').findOne(query, function(err, result){
        if (result != null) { //Si la consulta arrojo algun resultado y no es vacia
        console.log(`Nombre: ${result.nombre} Direccion: ${result.direccion}`)
        mensaje = {"_id": result._id,"nombre": result.nombre, "direccion": result.direccion, "ciudad": result.ciudad}
        return response.send(mensaje)        
        }
        
        return response.status(404).send({"mensaje": "No se ha encontrado el punto de venta, recuerde que los valores de entrada deben ser exactos"}) //La consulta ha sido vacia
    })
});

//PUT: Actualizar la informacion de un punto de venta
app.put(rutas["actualizarpunto"], (request, response) => {
    //Confirmar que hay datos en el cuerpo de la peticion
    if (Object.keys(request.body).length === 0) {
        return response.status(400).send({"mensaje": "El cuerpo de la peticion está vacio"})
    }    
    //Operacion sobre la base de datos
    db.collection('puntos').findOneAndUpdate({"ciudad": request.params.ciudad, "direccion": request.params.direccion}, {$set: request.body}, {returnNewDocument:true}, function(err, result){
        if (err) {
            mensaje = {"mensaje": "Error ejecutando la actualizacion", "error": err}
            return response.status(500).send(mensaje)
        }
        else if (result != null) { //El elemento existe y su actualizacion se realizo con exito 
            mensaje = {"mensaje":"Actualizacion realizada con exito"}
            return response.send(mensaje)
        }
        //El elemento a actualizar no existe
        return response.status(404).send({"mensaje": "No se ha encontrado el punto de venta para actualizar, recuerde que los valores de entrada deben ser exactos"}) //La consulta ha sido vacia
    });
});

//DELETE: Elimina un punto de venta
app.delete(rutas["eliminarpunto"], (request, response) => {
    //Operacion de eliminacion sobre la DB
    db.collection('puntos').findOneAndDelete({$and:[{"ciudad": request.params.ciudad}, {"direccion": request.params.direccion}]}, function(err, result) {
        if (err) {
            mensaje = {"mensaje": "Error ejecutando la eliminacion", "error": err}
            return response.status(500).send(mensaje)
        }
        else if (result.value != null) { //El elemento existe y su actualizacion se realizo con exito
            console.log(result)            
            mensaje = {"mensaje":"Eliminacion realizada con exito", "datosEliminados": result.value}
            return response.send(mensaje)
        }
        //El elemento a actualizar no existe
        return response.status(404).send({"mensaje": "No se ha encontrado el punto de venta para eliminar, recuerde que los valores de entrada deben ser exactos"}) //La consulta ha sido vacia
    })
});