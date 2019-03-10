from django.urls import path
from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    url('^$', views.index),
    url(r'^darproductos/', views.darProductos), #Vista asociada
    url(r'^crearproducto/$', csrf_exempt(views.crearProducto), name='crearPorducto'),    
]