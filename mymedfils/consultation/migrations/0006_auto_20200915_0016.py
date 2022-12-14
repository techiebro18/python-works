# Generated by Django 3.1.1 on 2020-09-14 18:46

import consultation.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultation', '0005_consultation_treatment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultationimage',
            name='file',
            field=models.FileField(upload_to='static/consultation_files/', validators=[consultation.validators.validate_file_extension]),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(blank=True, choices=[('', 'Choose Treatment Type'), ('homeopathic', 'Homeopathic'), ('ayurvedic', 'Ayurvedic'), ('unani', 'Unani')], max_length=30)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
