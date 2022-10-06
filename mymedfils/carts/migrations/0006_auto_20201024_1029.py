# Generated by Django 3.1.1 on 2020-10-24 04:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_auto_20201017_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('code', models.CharField(max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=50)),
                ('is_percent', models.BooleanField(default=False)),
                ('expiry', models.DateField(blank=True)),
                ('is_forever', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='carts.coupon'),
        ),
    ]