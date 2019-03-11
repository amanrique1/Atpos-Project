from django.db import models

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