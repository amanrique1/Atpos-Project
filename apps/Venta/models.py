from django.db import models
from django.forms.models import model_to_dict

# Create your models here.
class Factura(models.Model):
	fecha=models.DateField()
	metodoDePago=models.CharField(max_length=30)
	pagado=models.BooleanField()
	usuario = models.CharField(max_length=256, null=False)
	pago = models.PositiveIntegerField(null=True)

	def as_json(self):
		datos = model_to_dict(self, fields=[fields.name for fields in self._meta.fields]) #Poner en un diccionario los datos principales de la factura
		ventaProducto = [venta.as_json() for venta in self.venta_set.all()]#Pedir todos los productos que se vendieron en esa factura
		datos["productos-vendidos"] = ventaProducto
		return datos

class Venta(models.Model):
	class Meta:
		unique_together = ('especificacionProducto', 'factura')        
	especificacionProducto=models.CharField(max_length=256, null=False)
	factura=models.ForeignKey(Factura,null=False,blank=True,on_delete=models.CASCADE)
	cantidad=models.IntegerField()

	def as_json(self):
		return model_to_dict(self, fields=[fields.name for fields in self._meta.fields])
