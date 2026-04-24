from django.contrib import admin
from .models import Doctor

# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'experience')
    
admin.site.register(Doctor, DoctorAdmin)
