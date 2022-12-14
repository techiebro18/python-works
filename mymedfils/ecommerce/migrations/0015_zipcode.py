# Generated by Django 3.1.1 on 2021-02-24 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultation', '0017_specialist'),
        ('ecommerce', '0014_auto_20210103_1624'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zipcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zipcode', models.CharField(max_length=10)),
                ('cod', models.BooleanField(default=True)),
                ('delivery_charge', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='consultation.city')),
            ],
        ),
    ]
