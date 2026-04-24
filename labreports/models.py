from django.db import models
from django.conf import settings
from patients.models import Patient
from doctors.models import Doctor

User = settings.AUTH_USER_MODEL

# Create your models here.
class LabReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    report_file = models.FileField(upload_to='lab_reports/')
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report for {self.patient}"
    
