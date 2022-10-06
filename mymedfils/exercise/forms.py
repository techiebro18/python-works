from django import forms
from django.forms import ModelForm
from .models import Member
from django.utils.translation import gettext_lazy as _

GROUPS = [
	('', 'Select Type'),
	('Doctors', 'Doctor'),
	('Nurses', 'Nurse')
	]

class MemberForm(ModelForm):
	type = forms.ChoiceField(choices=GROUPS)
	class Meta:
		model = Member
		fields = ['name', 'email', 'mobile']
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your name'}),
			'email': forms.EmailInput(attrs={'class':'form-control'}),
			'mobile': forms.NumberInput(attrs={'class':'form-control'}),
			'type': forms.Select(attrs={'class':'form-control'})
		}
		lables = {
			'type': _(''),
			'name': _(''),
		}