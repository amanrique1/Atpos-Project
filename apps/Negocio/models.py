from django.db import models

# Create your models here.
class PuntoDeVenta(models.Model):
	nombre=models.CharField(max_length=30)
	ciudad=models.CharField(max_length=30)
	direccion = models.TextField()
	def __str__(self):
		return '{}'.format(self.nombre)

class PuntoDeVentaProds(models.Model):
	class Meta:
		unique_together = ('puntoDeVenta', 'especificacionProducto')

	puntoDeVenta=models.OneToOneField(PuntoDeVenta,null=False,blank=True,on_delete=models.CASCADE)
	especificacionProducto=models.ForeignKey(EspecificacionProducto,null=True,blank=True,on_delete=models.CASCADE)
	cantidad=models.IntegerField()
