from django import forms
from django.forms import ModelForm
from .models import Consultation, ConsultationImage, Profile, User
from django.utils.translation import gettext_lazy as _

GENDER_CHOICES = [
    ('', 'Gender'),
    ('male', 'Male'),
    ('female', 'Female')
]
MARITAL_STATUSES = [
    ('', 'Marital Status'),
    ('single', 'Single'),
    ('married', 'Married')
]

class ConsultationForm(ModelForm):
    
    class Meta:
        model = Consultation
        fields = ('treatment_type', 'name', 'email', 'mobile', 'age', 'gender', 'marital_status', 'height', 'weight', 'problem', 'history', 'problem_time', 'allergic_problem', 'current_treatment')
        widgets = {
            'treatment_type': forms.Select(attrs={'class':'', 'placeholder':''}),
            'name': forms.TextInput(attrs={'class':'', 'placeholder':''}),
            'email': forms.EmailInput(attrs={'class':'', 'placeholder':''}),
            'mobile': forms.TextInput(attrs={'class':'','placeholder':''}),
            'age': forms.NumberInput(attrs={'class':'','placeholder':''}),
            'gender': forms.Select(attrs={'class':'cls-select'}),
            'marital_status': forms.Select(attrs={'class':'cls-select'}),
            'height': forms.TextInput(attrs={'class':'', 'placeholder':''}),
            'weight': forms.TextInput(attrs={'class':'', 'placeholder':''}),
            #'problem': forms.TextInput(attrs={'class':'', 'placeholder':'Write/Describe Your Problem'}),
            'problem': forms.Textarea(attrs={'rows':0, 'cols':0, 'class':'', 'placeholder':''}),
            'history': forms.TextInput(attrs={'class':'', 'placeholder':''}),
            'problem_time': forms.Textarea(attrs={'rows':0, 'cols':0, 'class':'', 'placeholder':''}),
            'allergic_problem': forms.Textarea(attrs={'rows':0, 'cols':0, 'class':'', 'placeholder':''}),
            'current_treatment': forms.Textarea(attrs={'rows':0, 'cols':0, 'class':'', 'placeholder':''}),
        }
        labels = {
            'treatment_type': _(''),
            'name': _(''),
            'email': _(''),
            'mobile': _(''),
            'age': _(''),
            'gender': _(''),
            'marital_status': _(''),
            'height': _(''),
            'weight': _(''),
            'problem': _(''),
            'history': _(''),
            'problem_time': _(''),
            'allergic_problem': _(''),
            'current_treatment': _(''),
        }


class ConsultationImageForm(ModelForm):

    class Meta:
        model = ConsultationImage
        fields = ('file',)
        widgets = {
            'file': forms.ClearableFileInput(attrs={'multiple': True})
        }
        labels = {
            'file': _('Upload Multiple Files (Keep `CTRL` pressed + Choose Files)')
        }


class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email address must be unique.')
        return email


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('user_type', 'bio')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'', 'placeholder':''}))



    
""" class ConsultationForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Name'}), label='')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'', 'placeholder':'Email'}), label='')
    mobile = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'','placeholder':'Mobile'}), label='')
    age = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'','placeholder':'Age'}), label='')
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class':'cls-select'}), label='')
    marital_status = forms.ChoiceField(choices=MARITAL_STATUSES, widget=forms.Select(attrs={'class':'cls-select'}), label='')
    height = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Height'}), label='') 
    weight = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Weight'}), label='') 
    problem = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Write/Describe Your Problem'}), label='') 
    history = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Past History If Any'}), label='') 
    problem_time = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'How long is the problem'}), label='') 
    allergic_problem = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':'Mention If Any Allergic Problem You have'}), label='')
    current_treatment = forms.CharField(widget=forms.Textarea(attrs={'class':'', 'placeholder':'Current Treatment If Any'}), label='')
    uploaded_files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label="Upload Files")
 """    