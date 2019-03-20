from django.db import models
from apps.Negocio.models import PuntoDeVenta
from apps.Venta.models import Factura

# Create your models here.

class Producto(models.Model):
	codigoBarras= models.CharField(max_length=30)
	nombre= models.CharField(max_length=70)
	cantidadMedida= models.IntegerField()
	unidadMedida= models.CharField(max_length=10)
	descripcion= models.TextField()
	marca= models.CharField(max_length=50)

class EspecificacionProducto(models.Model):

	idEspecificacionProducto=models.CharField(primary_key=True,max_length=50)
	precio=models.FloatField()
	precioUnidadMedida=models.FloatField()
	fechaVencimiento=models.DateField()
	producto=models.OneToOneField(Producto,null=False,blank=True,on_delete=models.CASCADE)
	lote=models.ForeignKey(Lote,null=False,blank=True)
	puntoDeVenta=models.ForeignKey(PuntoDeVenta,null=False,blank=True,on_delete=models.CASCADE)
	

class TipoDeProducto(models.Model):
	nombreTipo=models.CharField(primary_key=True,max_length=50)
	metodoAlmacenamiento=models.CharField(max_length=50)

class Categoria(models.Model):
	nombreCategoria=models.CharField(primary_key=True,max_length=50)
	perecedero=models.BooleanField()

class Lote(models.Model):
	fechaVencimiento=models.DateField()