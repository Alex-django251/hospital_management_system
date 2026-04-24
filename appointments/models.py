from django.db import models
from django.core.exceptions import ValidationError
from datetime import time
import datetime
from patients.models import Patient
from doctors.models import Doctor


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    def __str__(self):
        return f"{self.patient.user.username} -> {self.doctor.user.username} - {self.date} - {self.time}"

    def clean(self):
        if self.date < datetime.date.today():
            raise ValidationError("Cannot book appointment in the past")
        if self.time < time(9, 0) or self.time > time(17, 0):
            raise ValidationError("Appointment time must be between 9 AM and 5 PM")

    class Meta:
        unique_together = ('doctor', 'date', 'time')