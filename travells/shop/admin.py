from django.contrib import admin
from .models import Service, Contact

# Register your models here.
admin.site.register(Service)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'subject')

    class Meta:
        model=Contact

admin.site.register(Contact, ContactAdmin)