from django.db import models
from django.conf import settings
from appointments.models import Appointment
from doctors.models import Doctor
from patients.models import Patient

User = settings.AUTH_USER_MODEL

# Create your models here.
class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medicines = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prescription for {self.patient} by {self.doctor}"
    
