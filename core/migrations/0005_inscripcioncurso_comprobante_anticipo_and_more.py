# Generated by Django 5.1.3 on 2024-11-17 04:11

import core.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_inscripcioncurso_estado_alter_pedido_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscripcioncurso',
            name='comprobante_anticipo',
            field=models.FileField(blank=True, help_text='Sube el comprobante de pago del anticipo', null=True, upload_to=core.models.comprobante_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]),
        ),
        migrations.AddField(
            model_name='pedido',
            name='comprobante_anticipo',
            field=models.FileField(blank=True, help_text='Sube el comprobante de pago del anticipo', null=True, upload_to=core.models.comprobante_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]),
        ),
        migrations.AddField(
            model_name='reserva',
            name='comprobante_anticipo',
            field=models.FileField(blank=True, help_text='Sube el comprobante de pago del anticipo', null=True, upload_to=core.models.comprobante_directory_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])]),
        ),
    ]
