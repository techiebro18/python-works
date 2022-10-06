from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from .models import Service, Contact
from django.urls import reverse
from django.contrib import messages

# Create your views here.
def home(request):
    services = get_services()
    context = {
        'title': 'Home | Naushad Tour & Travells',
        'services': services
    }
    return render(request, "shop/index.html", context)


def contactus(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        try:
            contact_obj = Contact.objects.create(
                name = name,
                phone = phone,
                email = email,
                subject = subject,
                message = message
            )
            if contact_obj:
                messages.success(request, 'Message sent successfully!')
                return redirect('/contact-us/')
        except Exception:
            print("Something Went Wrong!")
            
    else:
        context = {
            'title': 'Contact Us'
        }
        return render(request, "shop/contact.html", context)


def aboutus(request):
    context = {
        'title': 'About Us'
    }
    return render(request, "shop/aboutus.html", context)


def team(request):
    context = {
        'title': 'Team'
    }
    return render(request, "shop/team.html", context)


def get_services():
    services = Service.objects.filter(status=True).all()
    return services