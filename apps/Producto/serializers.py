from rest_framework import serializers
from . import models

class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('codigoBarras', 'nombre', 'cantidadMedida', 'unidadMedida', 'descripcion', 'marca')
        model = models.Producto