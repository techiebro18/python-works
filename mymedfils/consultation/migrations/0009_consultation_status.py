# Generated by Django 3.1.1 on 2020-09-19 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0008_auto_20200919_1245'),
    ]

    operations = [
        migrations.AddField(
            model_name='consultation',
            name='status',
            field=models.CharField(choices=[(0, 'Inactive'), (1, 'Active')], default='1', max_length=1),
        ),
    ]
