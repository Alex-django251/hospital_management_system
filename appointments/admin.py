from django.contrib import admin
from .models import Appointment

# Register your models here.
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    
    def save_model(self, request, obj, form, change):
        obj.full_clean()
        super().save_model(request, obj, form, change)
        
admin.site.register(Appointment, AppointmentAdmin)


