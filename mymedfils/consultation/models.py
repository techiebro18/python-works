from django.db import models
from .validators import validate_file_extension
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


GENDER_CHOICES = [
    ('', 'Gender'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
]
MARITAL_STATUSES = [
    ('', 'Marital Status'),
    ('single', 'Single'),
    ('married', 'Married')
]
TREATMENT_TYPE = [
    ('', 'Choose Treatment Type'),
    ('homeopathic', 'HOMEOPATHY'),
    ('ayurvedic', 'AYURVEDA'),
    ('unani', 'UNANI'),
    ('diet_nutritions', 'DIET & NUTRITIONS'),
]
STATUSES = [
    ('0', 'Inactive'),
    ('1', 'Active')
]
RESPONSE_TYPE = [
    ('answered', 'Answered'),
    ('rejected', 'Rejected')
]

# Create your models here.
class Consultation(models.Model):
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPE)
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    mobile = models.CharField(max_length=12)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=10, choices=MARITAL_STATUSES, blank=True)
    height = models.CharField(max_length=10, blank=True) 
    weight = models.CharField(max_length=10) 
    problem = models.TextField() 
    history = models.TextField(blank=True) 
    problem_time = models.TextField() 
    allergic_problem = models.TextField(blank=True)
    current_treatment = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='1')
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


class ConsultationImage(models.Model):
    file = models.FileField(upload_to="static/consultation_files/", validators=[validate_file_extension], blank=True)
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)

    def __str__(self):
        return self.consultation.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=30, choices=TREATMENT_TYPE, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    billing_name = models.CharField(max_length=255, blank=True, null=True)
    billing_email = models.EmailField(max_length=255, blank=True, null=True, unique=True)
    billing_mobile = models.CharField(max_length=12, blank=True, null=True, unique=True)
    billing_address = models.CharField(max_length=255, blank=True, null=True)
    billing_postcode = models.CharField(max_length=6, blank=True, null=True)
    billing_city = models.CharField(max_length=100, blank=True, null=True)
    billing_state = models.CharField(max_length=100, blank=True, null=True)
    billing_country = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        if self.user.first_name != '':
            return self.user.first_name 
        else:
            return self.user.username


class Specialist(models.Model):
    name = models.CharField(max_length=150)
    experience = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='static/consultation_files/specialists/', blank=True)
    status = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ConsultationResponse(models.Model):
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE)
    response = models.TextField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response_type = models.CharField(max_length=10, choices=RESPONSE_TYPE, default='answered')
    date = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.consultation.email+': '+self.user.first_name+': '+self.response_type




class Country(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class State(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class City(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


