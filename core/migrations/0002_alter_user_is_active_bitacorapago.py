# Generated by Django 5.1.3 on 2024-11-19 01:53

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.CreateModel(
            name='BitacoraPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_compra', models.CharField(choices=[('curso', 'Curso'), ('servicio', 'Servicio'), ('producto', 'Producto')], max_length=20)),
                ('id_compra', models.PositiveIntegerField()),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_pago', models.DateTimeField(default=django.utils.timezone.now)),
                ('estado', models.CharField(max_length=50)),
                ('detalles', models.TextField(blank=True, null=True)),
                ('metodo_pago', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.metodopago')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_pago'],
            },
        ),
    ]
