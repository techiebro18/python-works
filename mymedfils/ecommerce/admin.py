from django.contrib import admin
from .models import PaymentMethod, ShippingMethod, Slider, Page, ContactUs, Subscribe, Zipcode
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(ShippingMethod)
admin.site.register(Slider)
admin.site.register(Page)
admin.site.register(ContactUs)
admin.site.register(Subscribe)


class ZipcodeAdmin(ImportExportModelAdmin):
    list_display = ['__str__', 'city_name', 'state_name', 'cod', 'delivery_charge', 'days', 'status']
    search_fields = ('zipcode',)

    class Meta:
        model = Zipcode

    def city_name(self, obj):
        return obj.city

    def state_name(self, obj):
        return obj.city.state

admin.site.register(Zipcode, ZipcodeAdmin)
