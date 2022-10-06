from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from ecommerce.models import ContactUs


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    #username = forms.CharField(max_length=150, unique=True)
    #mobile = forms.IntegerField()

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2',)
        widgets = {
            'email': forms.EmailInput(attrs={'class':'', 'placeholder':'Email'}),
            #'mobile': forms.NumberInput(attrs={'class':'', 'placeholder':'Mobile'}),
            'username': forms.TextInput(attrs={'class':'', 'placeholder':'Username'}),
            'password1': forms.TextInput(attrs={'class':'', 'placeholder':'Password'}),
            'password2': forms.TextInput(attrs={'class':'', 'placeholder':'Confirm Password'})
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email address must be unique.')
        return email


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'class':'', 'placeholder':''}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'', 'placeholder':''}))


class MyaccountForm(forms.Form):
    username = forms.CharField(max_length=254)
    first_name = forms.CharField(max_length=254)
    last_name = forms.CharField(max_length=254)
    email = forms.EmailField(max_length=254)
    mobile = forms.IntegerField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'mobile',)
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'mobile': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Mobile'}),
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'})
        }

    def __init__(self, *args, **kwargs):
        super(MyaccountForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email address must be unique.')
        return email


class ContactUsForm(forms.ModelForm):

    class Meta:
        model = ContactUs
        fields = ('name', 'email', 'mobile', 'purpose', 'message',)

    """ def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile') """
        