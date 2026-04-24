from django.db import models
from appointments.models import Appointment

# Create your models here.
class Invoice(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    medicine_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        self.total_amount = (self.consultation_fee + self.medicine_charges + self.lab_charges)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Invoice {self.id} - {self.total_amount}"
    
    