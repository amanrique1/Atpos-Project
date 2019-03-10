# Generated by Django 2.1.5 on 2019-03-10 04:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Producto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EspecificacionProducto',
            fields=[
                ('idEspecificacionProducto', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('precio', models.FloatField()),
                ('precioUnidadMedida', models.FloatField()),
                ('fechaVencimiento', models.DateField()),
                ('producto', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, to='Producto.Producto')),
            ],
        ),
    ]
