//Sección de librerias, el requiere indica que al ejecutar se necesita el paquete en especifico
const express = require('express')
const app = express() //Invoca las funciones de la libreria express para su posterior uso.
const PUERTO = 3000 //Puerto de ejecucion
const bodyParser = require('body-parser') //Parser para el cuerpo de las peticiones

//Configura el parser para formato JSON
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); // support json encoded bodies

//Diccionario con las rutas de los recursos de la aplicacion
const rutas = {
    "crearpunto" : "/crearpunto",
    "darpunto": "/darpunto",
    "actualizarpunto": "/actualizarpunto",
    "eliminarpunto": "/eliminarpunto"
}

//Etiquetas para el formato del json con los datos.
const formato = ["nombre", "ciudad", "direccion"]

//Configura el puerto de despliegue de la aplicacion, el siguiente parametro es una funcion
//con la que esperamos recibir parametros y ejecutar.
app.listen(PUERTO, function(){
    console.log(`Prueba correcta en el puerto ${PUERTO}`)
})

//Permite confirmar que el cuerpo de la peticion posee todos los valores solicitados para hacer un post
function confirmarCuerpo(datos) {
    camposFaltantes = {} //Diccionario para responder los campos que faltan 
    
    if (Object.keys(datos).length === 0) return false
    
    for(const clave of formato) {
        if(datos.clave === null || typeof datos.clave != 'string') {
            camposFaltantes[clave] = "El valor no existe o no esta dado en el formato correcto"
        }
    }  
    
    return camposFaltantes
}

//Mensaje raiz para el indice
app.get('/', (request, response) => {
    let ruta = JSON.stringify(rutas) //Acceso a variable global
    let mensaje = "Bienvenido al microservicio de puntos de venta del negocio, rutas disponibles \n\n"    
    response.send(mensaje.concat(ruta))    
})


//Operaciones CRUD.

//POST
app.post(rutas["crearpunto"], (request, response) => {
    console.log(request.body)
    confirmado = confirmarCuerpo(request.body)
    if (confirmado === false) {
        mensaje = {"mensaje": "El cuerpo del mensaje está vacio"}
        response.send(mensaje)
    }

    else {
        response.send(confirmado)
    }    
})
