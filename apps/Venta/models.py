from django.db import models
from apps.Producto.models import EspecificacionProducto

# Create your models here.
class Caja(models.Model):

class Factura(models.Model):
	fecha=models.DateField()
	metodoDePago=models.CharField(max_length=30)
	pagado=models.BooleanField()

class Venta(models.Model):
	class Meta:
        unique_together = (('especificacionProducto', 'factura'),)
        
	especificacionProducto=models.ForeignKey(EspecificacionProducto,null=False,blank=True)
	factura=models.OneToOne(Factura,null=False,blank=True,on_delete=models.CASCADE)
	cantidad=models.IntegerField()
