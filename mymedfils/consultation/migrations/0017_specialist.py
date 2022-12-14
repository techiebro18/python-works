# Generated by Django 3.1 on 2021-02-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0016_auto_20201025_1254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Specialist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('experience', models.CharField(max_length=80)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, upload_to='static/consultation_files/specialists/')),
                ('status', models.BooleanField(default=True)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
