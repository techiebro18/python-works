# Generated by Django 3.1.1 on 2021-01-03 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0010_auto_20201227_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='name',
            field=models.CharField(default='Slider', max_length=100),
        ),
    ]
