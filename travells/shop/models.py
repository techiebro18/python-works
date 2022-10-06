from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime

# Create your models here.
class Service(models.Model):
    name = models.CharField(max_length=100)
    #description = models.TextField()
    description = RichTextUploadingField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=12)
    email = models.EmailField(max_length=100, blank=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

        