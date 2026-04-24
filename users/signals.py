from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from doctors.models import Doctor
from patients.models import Patient


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'doctor':
            Doctor.objects.create(user=instance)
        elif instance.role == 'patient':
            Patient.objects.create(user=instance)
            
            