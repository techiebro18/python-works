# Generated by Django 3.1.1 on 2022-07-05 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('mobile', models.IntegerField(max_length=11)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]