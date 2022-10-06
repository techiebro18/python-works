from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, Group
from .forms import MemberForm
from django.core import exceptions
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def home(request):
	user = User.objects.get(pk=13)
	#print(user.user_permissions.all())
	#return HttpResponse("Welcome to home")
	member_form = MemberForm()
	if request.method == "POST":
		member_form = MemberForm(request.POST)
		if member_form.is_valid():
			name = member_form.cleaned_data.get('name')
			email = member_form.cleaned_data.get('email')
			mobile = member_form.cleaned_data.get('mobile')
			group = member_form.cleaned_data.get('type')
			try:
				user_obj = User.objects.create_user(name, email=email, password="P@ssw0rd1111")
				user_obj.is_active = True
				group_obj = Group.objects.get(name=group)
				user_obj.groups.add(group_obj)
				user_obj.save()
				messages.success(request, "Member has been created successfully!")
				return HttpResponseRedirect(reverse('exercise:home'))
			except Exception as e:
				print(e)

		else:
			context = {
				'form': member_form
			}
			return render(request, "index.html", context)
	
	context = {
		"user": user,
		"user_permissions": user.user_permissions.all(),
		'form': member_form
	}
	return render(request, "index.html", context)
