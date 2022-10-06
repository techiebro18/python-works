from django.db import models
from consultation.validators import validate_file_extension
from datetime import datetime
from django.contrib.auth.models import User
from consultation.models import City

## This line makes email field unique all over the project even in admin panel
User._meta.get_field('email')._unique = True


PURPOSE_CHOICES = [
    ('General Enquiries', 'General Enquiries'),
    ('Business Opportunities', 'Business Opportunities'),
    ('Compliments/Testimonials', 'Compliments/Testimonials'),
    ('Incomplete Order', 'Incomplete Order'),
    ('Marketing Opportunities', 'Marketing Opportunities'),
    ('New Drug/ Product enquiry / New strength', 'New Drug/ Product enquiry / New strength'),
    ('Order Not Received', 'Order Not Received'),
    ('Payment Issues', 'Payment Issues'),
    ('Reward Program', 'Reward Program'),
    ('Upload Prescription Issues', 'Upload Prescription Issues'),

]

# Create your models here.
class ShippingMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    charge = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    status = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    charge = models.FloatField(default=0.00)
    status = models.BooleanField(default=True)
    default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Slider(models.Model):
    name = models.CharField(max_length=100, default='Slider')
    image = models.ImageField(upload_to='slider/', validators=[validate_file_extension])
    url   = models.CharField(max_length=200, blank=True)
    text  = models.CharField(max_length=150, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name 



class Page(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    content = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name


class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mobile = models.CharField(max_length=12)
    purpose = models.CharField(max_length=200, choices=PURPOSE_CHOICES)
    message = models.TextField()

    def __str__(self):
        return self.name



class Subscribe(models.Model):
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email


class Zipcode(models.Model):
    zipcode = models.CharField(max_length=10, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    cod = models.BooleanField(default=True)
    delivery_charge = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    days = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.zipcode

