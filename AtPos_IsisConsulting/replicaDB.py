import threading
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db import DatabaseError, OperationalError

"""
Crea un objeto que trabaja en un Thread para vaciar paralelamente la DB auxiliar
y mandar las peticiones a la maestra cuando hay conexion

"""






