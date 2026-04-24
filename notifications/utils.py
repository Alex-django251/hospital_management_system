from django.core.mail import send_mail
from django.conf import settings

def send_appointment_email(email, message):
    send_mail(
        subject="Hospital Appointment",
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )
    
    