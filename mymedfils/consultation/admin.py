from django.contrib import admin
from .models import Consultation, ConsultationImage, Profile, ConsultationResponse, Country, State, City, Specialist
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Profile)
admin.site.register(ConsultationResponse)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Specialist)

class ConsultationImageAdmin(admin.StackedInline):
    model = ConsultationImage

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    inlines = [ConsultationImageAdmin]

    class Meta:
        model = Consultation

@admin.register(ConsultationImage)
class ConsultationImageAdmin(admin.ModelAdmin):
    pass


#Cities admin
class CityAdmin(ImportExportModelAdmin):

    class Meta:
        model = City

admin.site.register(City, CityAdmin)