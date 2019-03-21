from django.db import models

# Create your models here.
class PuntoDeVenta(models.Model):
	nombre=models.CharField(max_length=30)
	ciudad=models.CharField(max_length=30)
	direccion = models.TextField()
	def __str__(self):
		return '{}'.format(self.nombre)

