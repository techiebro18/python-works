# Generated by Django 3.1.1 on 2020-10-31 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20201031_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]