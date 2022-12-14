# Generated by Django 3.1.1 on 2020-10-25 12:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_slider'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
                ('content', models.TextField(blank=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
