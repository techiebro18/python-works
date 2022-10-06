# Generated by Django 3.1.1 on 2020-10-19 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0013_auto_20201010_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='billing_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_country',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_email',
            field=models.EmailField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_mobile',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_postcode',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='billing_state',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
