# Generated by Django 3.1.1 on 2020-10-21 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_auto_20201020_2343'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=60),
            preserve_default=False,
        ),
    ]
